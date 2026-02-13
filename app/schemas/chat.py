"""
Pydantic schemas for chat requests and responses.
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class ChatRequest(BaseModel):
    """Request schema for chat endpoint with multilingual support."""
    model_config = ConfigDict(protected_namespaces=(), json_schema_extra={
        "example": {
            "message": "What are the symptoms of a brain tumor?",
            "language": "auto",
            "prediction_label": "Glioma Tumor",
            "confidence_score": 0.95
        }
    })
    
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    language: Literal["auto", "en", "hi", "te"] = Field("auto", description="Language: auto (detect), en (English), hi (Hindi), te (Telugu)")
    prediction_label: str | None = Field(None, description="Predicted tumor type from MRI (e.g., 'Glioma Tumor')")
    confidence_score: float | None = Field(None, ge=0.0, le=1.0, description="Model confidence score (0.0-1.0)")


class ChatResponse(BaseModel):
    """Response schema for multilingual chat endpoint."""
    model_config = ConfigDict(protected_namespaces=(), json_schema_extra={
        "example": {
            "response": "Brain tumors are abnormal growths in the brain...",
            "language": "en",
            "source": "llm",
            "is_unrelated": False,
            "is_medical_alert": False
        }
    })
    
    response: str = Field(..., description="Bot response in detected/selected language")
    language: str = Field(default="en", description="Language code of response (en, hi, te)")
    source: str = Field(default="llm", description="Response source: 'llm', 'domain_filter', 'emergency', 'fallback', or 'error'")
    is_unrelated: bool = Field(default=False, description="True if question is unrelated to brain/MRI")
    is_medical_alert: bool = Field(default=False, description="True if emergency symptoms detected")
