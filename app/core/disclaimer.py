"""
Medical disclaimer for all responses.
"""

MEDICAL_DISCLAIMER = """
MEDICAL DISCLAIMER: 
This AI system is for educational purposes only and should NOT be used for medical diagnosis or treatment decisions. 
The information provided is not a substitute for professional medical advice. 
Always consult with qualified healthcare professionals for medical concerns.
"""


def get_disclaimer() -> str:
    """
    Get the medical disclaimer.
    
    Returns:
        Medical disclaimer text
    """
    return MEDICAL_DISCLAIMER
