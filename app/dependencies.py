"""
Dependency injection for FastAPI endpoints.
"""

from app.core.model_loader import ModelLoader
from app.config import settings

# Global model loader instance
_model_loader = None


def get_model_loader() -> ModelLoader:
    """
    Get or create the model loader instance (singleton pattern).
    
    Returns:
        ModelLoader: The model loader instance
    """
    global _model_loader
    if _model_loader is None:
        _model_loader = ModelLoader(settings.MODEL_NAME)
    return _model_loader
