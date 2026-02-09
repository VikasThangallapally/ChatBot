from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta, datetime, timezone
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.schemas.password_reset import ForgotPasswordRequest, ResetPasswordRequest, PasswordResetResponse
from app.core.auth import get_password_hash, create_access_token, authenticate_user, get_current_user, get_user_by_email
from app.config import settings
from app.db import supabase
from app.utils.logger import get_logger
from app.services.email_service import send_otp_email
import logging
import random
import string

logger = get_logger(__name__)
router = APIRouter()


@router.post("/register", response_model=UserOut, summary="Register new user")
async def register(user_in: UserCreate):
    """Register a new user in Supabase."""
    try:
        existing = get_user_by_email(user_in.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Insert user into Supabase
        response = supabase.table("users").insert({
            "name": user_in.name,
            "email": user_in.email,
            "password_hash": get_password_hash(user_in.password)
        }).execute()
        
        if response.data and len(response.data) > 0:
            user = response.data[0]
            return UserOut(id=user["id"], name=user["name"], email=user["email"])
        else:
            raise HTTPException(status_code=500, detail="Failed to create user in database")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Register error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login")
async def login(form_data: UserLogin):
    """Login user and return JWT token."""
    user = authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user."""
    return UserOut(id=current_user["id"], name=current_user["name"], email=current_user["email"])


@router.post("/auth/forgot-password", response_model=PasswordResetResponse, summary="Request password reset OTP")
async def forgot_password(request: ForgotPasswordRequest):
    """
    Generate and send OTP to user's email for password reset.
    OTP expires in 10 minutes.
    """
    try:
        # Verify user exists
        user = get_user_by_email(request.email)
        if not user:
            # Don't reveal whether email exists for security
            raise HTTPException(status_code=400, detail="If this email exists, you will receive an OTP shortly")
        
        # Generate 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        # Calculate expiry time (10 minutes from now) using timezone-aware UTC
        expiry_time = datetime.now(timezone.utc)
        from datetime import timedelta as td
        expiry_time = expiry_time + td(minutes=10)
        
        # Store OTP in Supabase
        response = supabase.table("password_reset_otps").insert({
            "user_email": request.email,
            "otp_code": otp_code,
            "expires_at": expiry_time.isoformat(),
            "is_used": False
        }).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to generate OTP")
        
        # Send OTP via email
        email_sent = send_otp_email(request.email, otp_code)
        
        if not email_sent:
            logger.warning(f"Failed to send OTP email to {request.email}, but OTP was generated")
            # Still return success since OTP was generated (user can get it from database in dev)
        
        logger.info(f"✅ OTP generated for {request.email}")
        return PasswordResetResponse(
            message="If this email exists, an OTP has been sent. Check your email.",
            status="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Forgot password error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process forgot password request")


@router.post("/auth/reset-password", response_model=PasswordResetResponse, summary="Reset password using OTP")
async def reset_password(request: ResetPasswordRequest):
    """
    Reset user password using OTP.
    Verifies OTP is valid, not expired, and not already used.
    """
    try:
        # Verify user exists
        user = get_user_by_email(request.email)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        
        # Fetch the OTP record
        otp_response = supabase.table("password_reset_otps").select("*").eq(
            "user_email", request.email
        ).eq("is_used", False).order("created_at", desc=True).limit(1).execute()
        
        if not otp_response.data or len(otp_response.data) == 0:
            raise HTTPException(status_code=400, detail="No active OTP found. Request a new one.")
        
        otp_record = otp_response.data[0]
        
        # Verify OTP code matches
        if otp_record["otp_code"] != request.otp_code:
            raise HTTPException(status_code=400, detail="Invalid OTP code")
        
        # Check if OTP has expired. Parse stored ISO timestamp and compare using timezone-aware datetimes
        expires_at_raw = otp_record.get("expires_at")
        try:
            # Normalize 'Z' to +00:00 then parse
            expires_at = datetime.fromisoformat(expires_at_raw.replace('Z', '+00:00'))
        except Exception:
            # Fallback: treat as naive UTC
            expires_at = datetime.fromisoformat(expires_at_raw)
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        now_utc = datetime.now(timezone.utc)
        logger.debug(f"OTP expires_at={expires_at.isoformat()} now_utc={now_utc.isoformat()}")
        if now_utc > expires_at:
            raise HTTPException(status_code=400, detail="OTP has expired. Request a new one.")
        
        # Verify OTP hasn't been used
        if otp_record["is_used"]:
            raise HTTPException(status_code=400, detail="This OTP has already been used")
        
        # Hash new password
        new_password_hash = get_password_hash(request.new_password)
        
        # Update user password in users table
        # Update only the password hash. Some Supabase projects may not have
        # an `updated_at` column in the `users` table; avoid updating it to
        # prevent PGRST204 schema errors.
        update_response = supabase.table("users").update({
            "password_hash": new_password_hash
        }).eq("email", request.email).execute()
        
        if not update_response.data:
            raise HTTPException(status_code=500, detail="Failed to update password")
        
        # Mark OTP as used
        supabase.table("password_reset_otps").update({
            "is_used": True
        }).eq("id", otp_record["id"]).execute()
        
        logger.info(f"✅ Password reset successfully for {request.email}")
        return PasswordResetResponse(
            message="Password has been reset successfully. Please login with your new password.",
            status="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reset password error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to reset password: {str(e)}")

