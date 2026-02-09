"""
Configuration module for loading environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings from environment variables."""
    
    # API settings
    API_TITLE = "Brain Tumor Chatbot"
    API_VERSION = "1.0.0"
    
    # Model settings
    MODEL_NAME = os.getenv("MODEL_NAME", "brain_tumor_model.h5")
    MODEL_REVISION = os.getenv("MODEL_REVISION", "main")
    
    # Image settings
    IMAGE_SIZE = int(os.getenv("IMAGE_SIZE", "224"))
    MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB
    
    # Upload directory
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "app/static/uploads")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Model confidence threshold
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://uluxzbfstcemaprjhyjl.supabase.co")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVsdXh6YmZzdGNlbWFwcmpoeWpsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDY0MjAwNiwiZXhwIjoyMDg2MjE4MDA2fQ.e8nHKwZjQzr4z-FtuyDxqPNAfkLoOhIVdIBlUsQss60")

    # Auth / JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "ae9d1e30-5bf2-423a-954c-13c8c759452a")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # Email / SendGrid Configuration (for password reset OTPs)
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
    SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "")


settings = Settings()
