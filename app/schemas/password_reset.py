"""Pydantic schemas for password reset"""

from pydantic import BaseModel, EmailStr


class ForgotPasswordRequest(BaseModel):
    """Request schema for forgot password endpoint"""
    email: EmailStr
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }


class ResetPasswordRequest(BaseModel):
    """Request schema for reset password endpoint"""
    email: EmailStr
    otp_code: str
    new_password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "otp_code": "123456",
                "new_password": "NewPassword123!"
            }
        }


class PasswordResetResponse(BaseModel):
    """Response schema for password reset operations"""
    message: str
    status: str
