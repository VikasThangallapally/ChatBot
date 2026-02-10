from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta, datetime, timezone
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.schemas.password_reset import ForgotPasswordRequest, ResetPasswordRequest, PasswordResetResponse
from app.core.auth import get_password_hash, create_access_token, authenticate_user, get_current_user, get_user_by_email
from app.config import settings
from app.db import get_users_collection, get_password_reset_otps_collection
from app.utils.logger import get_logger
from app.services.email_service import send_otp_email
from bson.objectid import ObjectId
import logging
import random
import string

logger = get_logger(__name__)
router = APIRouter()


@router.post("/register", response_model=UserOut, summary="Register new user")
async def register(user_in: UserCreate):
    """Register a new user in MongoDB."""
    try:
        users = get_users_collection()
        existing = users.find_one({"email": user_in.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Insert user into MongoDB
        user_doc = {
            "name": user_in.name,
            "email": user_in.email,
            "password_hash": get_password_hash(user_in.password),
            "created_at": datetime.now(timezone.utc)
        }
        result = users.insert_one(user_doc)
        
        if result.inserted_id:
            return UserOut(id=str(result.inserted_id), name=user_in.name, email=user_in.email)
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


@router.post("/logout")
async def logout():
    """Logout user (client-side token clearing)."""
    return {"message": "Logout successful", "status": "success"}


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
        users = get_users_collection()
        otps = get_password_reset_otps_collection()
        
        # Verify user exists
        user = users.find_one({"email": request.email})
        if not user:
            # Don't reveal whether email exists for security
            raise HTTPException(status_code=400, detail="If this email exists, you will receive an OTP shortly")
        
        # Generate 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        # Calculate expiry time (10 minutes from now) using timezone-aware UTC
        expiry_time = datetime.now(timezone.utc)
        from datetime import timedelta as td
        expiry_time = expiry_time + td(minutes=10)
        
        # Store OTP in MongoDB
        otp_doc = {
            "user_email": request.email,
            "otp_code": otp_code,
            "expires_at": expiry_time,
            "is_used": False,
            "created_at": datetime.now(timezone.utc)
        }
        result = otps.insert_one(otp_doc)
        
        if not result.inserted_id:
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
        users = get_users_collection()
        otps = get_password_reset_otps_collection()
        
        # Verify user exists
        user = users.find_one({"email": request.email})
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        
        # Fetch the OTP record - get the most recent unused OTP
        otp_record = otps.find_one({
            "user_email": request.email,
            "is_used": False
        }, sort=[("created_at", -1)])
        
        if not otp_record:
            raise HTTPException(status_code=400, detail="No active OTP found. Request a new one.")
        
        # Verify OTP code matches
        if otp_record["otp_code"] != request.otp_code:
            raise HTTPException(status_code=400, detail="Invalid OTP code")
        
        # Check if OTP has expired
        expires_at = otp_record.get("expires_at")
        now_utc = datetime.now(timezone.utc)
        
        if isinstance(expires_at, str):
            # Parse string timestamp if stored as string
            expires_at = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        
        logger.debug(f"OTP expires_at={expires_at.isoformat()} now_utc={now_utc.isoformat()}")
        if now_utc > expires_at:
            raise HTTPException(status_code=400, detail="OTP has expired. Request a new one.")
        
        # Verify OTP hasn't been used
        if otp_record.get("is_used", False):
            raise HTTPException(status_code=400, detail="This OTP has already been used")
        
        # Hash new password
        new_password_hash = get_password_hash(request.new_password)
        
        # Update user password in MongoDB
        users.update_one(
            {"email": request.email},
            {"$set": {"password_hash": new_password_hash, "updated_at": datetime.now(timezone.utc)}}
        )
        
        # Mark OTP as used
        otps.update_one(
            {"_id": otp_record["_id"]},
            {"$set": {"is_used": True}}
        )
        
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

