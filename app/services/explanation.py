"""
Explanation service for converting predictions to human-readable explanations.
"""

from typing import Dict, Any
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ExplanationService:
    """Service for generating human-readable explanations."""
    
    def __init__(self):
        """Initialize explanation service."""
        self.explanation_templates = {
            "high_confidence": (
                "The model has detected a high confidence match for '{label}' "
                "with {confidence}% confidence. "
                "This indicates {explanation}. "
                "Please consult with a medical professional for further evaluation."
            ),
            "medium_confidence": (
                "The model has detected a moderate confidence match for '{label}' "
                "with {confidence}% confidence. "
                "Additional analysis or expert review may be recommended."
            ),
            "low_confidence": (
                "The model's confidence is low ({confidence}%). "
                "The image may require re-examination or additional imaging studies."
            ),
            "no_match": (
                "No significant match was found in the analysis. "
                "The image may be unclear or additional imaging may be needed."
            )
        }
        
        self.label_explanations = {
            "tumor": "a potential tumor may be present",
            "normal": "the scan appears normal",
            "abnormality": "an abnormality has been detected",
            "cyst": "a cyst may be present",
            "edema": "brain swelling may be present"
        }
    
    def explain_prediction(self, prediction: Dict[str, Any]) -> str:
        """
        Generate explanation for a prediction.
        
        Args:
            prediction: Prediction result dictionary
            
        Returns:
            Human-readable explanation
        """
        try:
            if not prediction.get("predictions"):
                return self.explanation_templates["no_match"]
            
            top_prediction = prediction["predictions"][0]
            label = top_prediction["label"]
            confidence = top_prediction["percentage"]
            
            # Get label explanation
            label_explanation = self.label_explanations.get(
                label.lower(),
                f"results indicate {label}"
            )
            
            # Choose template based on confidence
            if confidence >= 80:
                template = self.explanation_templates["high_confidence"]
            elif confidence >= 50:
                template = self.explanation_templates["medium_confidence"]
            else:
                template = self.explanation_templates["low_confidence"]
            
            explanation = template.format(
                label=label,
                confidence=int(confidence),
                explanation=label_explanation
            )
            
            logger.info(f"Generated explanation for {label}")
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return "Unable to generate explanation for this prediction."
    
    def explain_response(self, response: str) -> str:
        """
        Generate explanation for a chat response.
        
        Args:
            response: Chat response text
            
        Returns:
            Additional explanation if needed
        """
        try:
            # For chat responses, provide context
            if any(keyword in response.lower() for keyword in ["tumor", "diagnosis", "treatment"]):
                return "This is general educational information only."
            
            return "Consult medical professionals for personalized advice."
            
        except Exception as e:
            logger.error(f"Error explaining response: {str(e)}")
            return "Information provided for educational purposes."
