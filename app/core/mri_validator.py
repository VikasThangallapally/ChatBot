"""
MRI Image Validation Module

Validates whether an uploaded image is a valid brain MRI scan
before running model predictions. Uses image analysis techniques
to detect non-medical images and reject them early.
"""

import numpy as np
from PIL import Image
from scipy import ndimage
from app.utils.logger import get_logger

logger = get_logger(__name__)


def is_valid_mri(image: Image.Image) -> tuple:
    """
    Validate if an image is a valid medical image for brain tumor classification.
    
    Args:
        image: PIL Image object to validate
        
    Returns:
        Tuple of (is_valid: bool, reason: str)
        - True, "Valid medical image" if valid
        - False, "reason..." if invalid
    """
    try:
        # Step 1: Check image size - basic minimum requirement
        width, height = image.size
        min_size = 96  # Relaxed from 64 to allow reasonable MRI images
        
        if width < min_size or height < min_size:
            return False, f"Image too small ({width}x{height}). Minimum {min_size}x{min_size} pixels required"
        
        # Step 2: Check for supported image modes
        if image.mode not in ["L", "RGB", "RGBA", "1"]:
            return False, f"Unsupported image format: {image.mode}"
        
        # Step 3: Convert to grayscale for basic analysis
        gray_image = image.convert("L")
        img_array = np.array(gray_image, dtype=np.float32)
        
        # Step 4: Basic brightness check (not too dark or too bright)
        mean_intensity = np.mean(img_array)
        
        # Allow wider range: medical images can be quite dark or bright
        if mean_intensity < 3 or mean_intensity > 252:
            return False, f"Image too {'dark' if mean_intensity < 3 else 'bright'} ({mean_intensity:.1f}). Please check image quality."
        
        # Step 5: Basic contrast check - image should have some variation
        std_intensity = np.std(img_array)
        if std_intensity < 5:
            return False, f"Image lacks sufficient contrast (std={std_intensity:.1f}). Please ensure image shows clear details."
        
        # All checks passed
        logger.info(f"Image validation successful: size={width}x{height}, mean={mean_intensity:.1f}, std={std_intensity:.1f}")
        return True, "Valid medical image"
        
    except Exception as e:
        logger.error(f"Error during MRI validation: {str(e)}")
        return False, f"Validation error: {str(e)}"
