"""Pydantic schemas for password reset"""

from pydantic import BaseModel, ConfigDict, EmailStr


class ForgotPasswordRequest(BaseModel):
    """Request schema for forgot password endpoint"""
    model_config = ConfigDict(protected_namespaces=(), json_schema_extra={
        "example": {
            "email": "user@example.com"
        }
    })
    
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Request schema for reset password endpoint"""
    model_config = ConfigDict(protected_namespaces=(), json_schema_extra={
        "example": {
            "email": "user@example.com",
            "otp_code": "123456",
            "new_password": "NewPassword123!"
        }
    })
    
    email: EmailStr
    otp_code: str
    new_password: str


class PasswordResetResponse(BaseModel):
    """Response schema for password reset operations"""
    message: str
    status: str
