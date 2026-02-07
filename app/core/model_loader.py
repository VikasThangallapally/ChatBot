"""
Model loader for Brain Tumor Classification.

Loads the trained TensorFlow/Keras model for brain tumor classification
from brain_tumor_model.h5. Uses lazy loading on first access.
"""

from typing import Optional
import os
from pathlib import Path
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ModelLoader:
    """Load and cache TensorFlow/Keras trained model."""
    
    def __init__(self, model_name: str = "brain_tumor_model.h5"):
        """
        Initialize the model loader.
        
        Args:
            model_name: Name of the model file
        """
        # Sanitize model name - extract filename if it contains slashes
        self.model_name = Path(model_name).name if "/" in model_name or "\\" in model_name else model_name
        # Ensure .h5 extension
        if not self.model_name.endswith(".h5"):
            self.model_name = "brain_tumor_model.h5"
        self.model_path = Path(__file__).parent.parent / "models" / self.model_name
        self._model = None
    
    def _load_model(self):
        """
        Load the TensorFlow/Keras model from disk.
        
        Uses lazy loading - model is only loaded when first accessed.
        """
        try:
            if not self.model_path.exists():
                raise FileNotFoundError(
                    f"Model file not found at {self.model_path}\n"
                    f"Please run training script first:\n"
                    f"  python training/train_model.py"
                )
            
            logger.info(f"Loading TensorFlow model from: {self.model_path}")
            import tensorflow as tf
            
            self._model = tf.keras.models.load_model(str(self.model_path))
            logger.info("Model loaded successfully")
            
            # Print model summary
            logger.info(f"Model input shape: {self._model.input_shape}")
            logger.info(f"Model output shape: {self._model.output_shape}")
            logger.info(f"Model parameters: {self._model.count_params():,}")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def get_model(self):
        """
        Get the loaded TensorFlow model.
        
        Returns:
            Loaded tf.keras.Model
        """
        if self._model is None:
            self._load_model()
        return self._model
    
    def get_pipeline(self):
        """
        Get the loaded model (for backward compatibility).
        
        Returns:
            Loaded tf.keras.Model
        """
        return self.get_model()
    
    def is_loaded(self) -> bool:
        """
        Check if model is loaded.
        
        Returns:
            True if model is loaded, False otherwise
        """
        return self._pipeline is not None
