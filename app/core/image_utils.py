"""
Image preprocessing utilities for Brain Tumor Classification.

Handles loading and preprocessing images to match training pipeline
(224x224 resize, normalization to [0,1]).
"""

from PIL import Image
import os
import numpy as np
from typing import Tuple
import tensorflow as tf
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ImageProcessor:
    """Process and preprocess images for model inference."""
    
    # Class indices mapping. Try to load from training folders if available
    # Fallback to default order used in the notebook.
    CLASS_INDICES = {}

    # Image size must match training (default from notebook)
    IMAGE_SIZE = settings.IMAGE_SIZE or 150

    @classmethod
    def _load_class_indices_from_training_folders(cls):
        """
        Attempt to discover class folders under `app/static/Brain Folders/Training`.
        If found, map folder names (sorted) to index -> pretty label.
        """
        try:
            base = os.path.join(os.getcwd(), "app", "static", "Brain Folders", "Training")
            if not os.path.exists(base):
                return False

            # List only directories
            folders = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
            if not folders:
                return False

            folders = sorted(folders)
            mapping = {}
            for idx, name in enumerate(folders):
                # Convert folder name to readable label
                label = name.replace("_", " ").title()
                mapping[idx] = label

            cls.CLASS_INDICES = mapping
            logger.info(f"Loaded class labels from training folders: {mapping}")
            return True
        except Exception as e:
            logger.warning(f"Failed to load training folder classes: {e}")
            return False


    # Initialize CLASS_INDICES at import time (best-effort)
    try:
        found = _load_class_indices_from_training_folders()
    except Exception:
        found = False

    if not found:
        # Default mapping if training folders not found
        CLASS_INDICES = {
            0: "Glioma Tumor",
            1: "Meningioma Tumor",
            2: "No Tumor",
            3: "Pituitary Tumor"
        }
    
    @staticmethod
    def load_image(file_path: str) -> Image.Image:
        """
        Load image from file path.
        
        Args:
            file_path: Path to image file
            
        Returns:
            PIL Image object
            
        Raises:
            ValueError: If image cannot be loaded
        """
        try:
            image = Image.open(file_path)
            logger.info(f"Image loaded: {file_path}")
            return image
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            raise ValueError(f"Cannot load image: {str(e)}")
    
    @staticmethod
    def preprocess_image(image: Image.Image, size: int | None = None) -> np.ndarray:
        """
        Preprocess image for CNN model inference.
        
        Matches the training preprocessing pipeline:
        1. Convert to RGB
        2. Resize to (150, 150) - matches notebook training
        3. Normalize pixel values to [0, 1]
        4. Add batch dimension
        
        Args:
            image: PIL Image object
            size: Target image size (default 150 to match training)
            
        Returns:
            Preprocessed numpy array with shape (1, 150, 150, 3)
        """
        try:
            # Use configured IMAGE_SIZE if not provided
            if size is None:
                size = ImageProcessor.IMAGE_SIZE

            # Convert to RGB if needed
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Resize image to match training input
            image = image.resize((size, size), Image.Resampling.LANCZOS)
            logger.info(f"Image resized to {size}x{size}")
            
            # Convert to numpy array
            image_array = np.array(image, dtype=np.float32)
            
            # Normalize to [0, 1] - matches training normalization
            image_array = image_array / 255.0
            
            # Add batch dimension: (224, 224, 3) -> (1, 224, 224, 3)
            image_array = np.expand_dims(image_array, axis=0)
            
            logger.info("Image preprocessed and normalized")
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise ValueError(f"Cannot preprocess image: {str(e)}")
    
    @staticmethod
    def get_image_info(image: Image.Image) -> dict:
        """
        Get image information.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with image info
        """
        return {
            "size": image.size,
            "mode": image.mode,
            "format": image.format
        }
    
    @staticmethod
    def get_class_name(class_index: int) -> str:
        """
        Map class index to class name.
        
        Args:
            class_index: Index of predicted class (0-3)
            
        Returns:
            Class name string
        """
        return ImageProcessor.CLASS_INDICES.get(class_index, "Unknown")

