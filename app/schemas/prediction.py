"""
Pydantic schemas for prediction requests and responses.
"""

from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class PredictionItem(BaseModel):
    """Single prediction item with class index."""
    class_index: int
    label: str
    confidence: float
    percentage: float


class TopPrediction(BaseModel):
    """Top prediction result."""
    class_index: int
    label: str
    confidence: float
    percentage: float


class MedicalAnalysis(BaseModel):
    """Detailed medical analysis for a tumor diagnosis."""
    tumor_type: str
    description: str
    advantages: List[str]
    disadvantages: List[str]
    key_characteristics: List[str]
    recommended_next_steps: List[str]
    severity_level: str


class BrainImageValidation(BaseModel):
    """Validation result for brain image detection."""
    is_valid_brain_image: bool
    confidence: float
    reason: str


class PredictionResponse(BaseModel):
    """Response schema for prediction endpoint."""
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra = {
            "example": {
                "predictions": [
                    {
                        "class_index": 0,
                        "label": "Glioma",
                        "confidence": 0.85,
                        "percentage": 85.0
                    },
                    {
                        "class_index": 3,
                        "label": "NoTumor",
                        "confidence": 0.10,
                        "percentage": 10.0
                    },
                    {
                        "class_index": 1,
                        "label": "Meningioma",
                        "confidence": 0.03,
                        "percentage": 3.0
                    },
                    {
                        "class_index": 2,
                        "label": "Pituitary",
                        "confidence": 0.02,
                        "percentage": 2.0
                    }
                ],
                "top_prediction": {
                    "class_index": 0,
                    "label": "Glioma",
                    "confidence": 0.85,
                    "percentage": 85.0
                },
                "image_path": "app/static/uploads/mri_scan.jpg",
                "model_version": "brain_tumor_model.h5",
                "status": "success",
                "disclaimer": "MEDICAL DISCLAIMER: This AI system is for educational purposes only..."
            }
        }
    )
    
    predictions: List[PredictionItem]
    top_prediction: Optional[TopPrediction] = None
    image_path: str
    model_version: Optional[str] = None
    status: str  # 'success', 'invalid_image', 'error'
    disclaimer: Optional[str] = None
    is_valid_brain_image: bool
    image_validation_confidence: float
    validation_reason: Optional[str] = None
    error: Optional[str] = None
    medical_analysis: Optional[MedicalAnalysis] = None
