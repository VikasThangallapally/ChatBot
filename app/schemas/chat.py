"""
Pydantic schemas for chat requests and responses.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    prediction_label: str | None = Field(None, description="Predicted tumor type from MRI (e.g., 'Glioma Tumor')")
    confidence_score: float | None = Field(None, ge=0.0, le=1.0, description="Model confidence score (0.0-1.0)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What are the symptoms of a brain tumor?",
                "prediction_label": "Glioma Tumor",
                "confidence_score": 0.95
            }
        }


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    response: str = Field(..., description="Bot response")
    explanation: str = Field(..., description="Additional explanation")
    source: str = Field(default="gpt", description="Response source: 'gpt', 'fallback', or 'error'")
    disclaimer: str = Field(..., description="Medical disclaimer")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Brain tumors are abnormal growths in the brain...",
                "explanation": "This is general educational information only.",
                "source": "gpt",
                "disclaimer": "MEDICAL DISCLAIMER: This AI system is for educational purposes only..."
            }
        }
