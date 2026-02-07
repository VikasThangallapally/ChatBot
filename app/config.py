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


settings = Settings()
