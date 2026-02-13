"""
Multilingual chat service with domain restriction and safety guardrails.
Handles GPT/LLM integration with language-aware responses.
"""

from openai import OpenAI
import os
from typing import Optional
from app.services.language_service import (
    LanguageService, 
    UNRELATED_RESPONSE,
    EMERGENCY_RESPONSE,
    MEDICAL_DISCLAIMER_PROMPTS
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MultilingualChatService:
    """Handles multilingual chat with domain restrictions and safety checks."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.openai_client = None
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if self.api_key:
            self.openai_client = OpenAI(api_key=self.api_key)
            logger.info("OpenAI client initialized")
        else:
            logger.warning("OPENAI_API_KEY not found, LLM features will be limited")
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available."""
        return self.openai_client is not None
    
    async def generate_response(
        self,
        user_message: str,
        language: str = "auto",
        prediction_label: Optional[str] = None,
        confidence_score: Optional[float] = None
    ) -> dict:
        """
        Generate multilingual response with domain restriction and safety guardrails.
        
        Args:
            user_message: User's message
            language: Language code (auto/en/hi/te)
            prediction_label: MRI prediction label
            confidence_score: Model confidence score
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Detect language if auto
            if language == "auto":
                detected_lang = LanguageService.detect_language(user_message)
                language_code = detected_lang
            else:
                language_code = LanguageService.get_language_code(language)
            
            logger.info(f"Processing message in language: {language_code}")
            
            # Check for emergency symptoms
            if LanguageService.check_emergency_symptoms(user_message, language_code):
                logger.warning("Emergency symptoms detected in user message")
                response = LanguageService.get_emergency_response(language_code)
                return {
                    "response": response,
                    "source": "emergency",
                    "language": language_code,
                    "is_medical_alert": True
                }
            
            # Quick keyword check for domain restriction
            if not LanguageService.is_brain_related(user_message, language_code):
                logger.info("Question appears unrelated to brain/MRI")
                response = LanguageService.get_unrelated_response(language_code)
                return {
                    "response": response,
                    "source": "domain_filter",
                    "language": language_code,
                    "is_unrelated": True
                }
            
            # Generate response using LLM if available
            if self.is_available():
                llm_response = await self._call_llm(
                    user_message=user_message,
                    language_code=language_code,
                    prediction_label=prediction_label,
                    confidence_score=confidence_score
                )
                
                if llm_response["success"]:
                    # Add medical disclaimer
                    response_with_disclaimer = llm_response["response"] + \
                                              LanguageService.get_medical_disclaimer(language_code)
                    
                    return {
                        "response": response_with_disclaimer,
                        "source": "llm",
                        "language": language_code,
                        "success": True
                    }
                else:
                    logger.warning(f"LLM call failed: {llm_response.get('error')}")
            
            # Fallback response if LLM unavailable
            fallback = self._get_fallback_response(language_code)
            return {
                "response": fallback,
                "source": "fallback",
                "language": language_code,
                "success": False
            }
            
        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}")
            return {
                "response": "An error occurred while processing your request.",
                "source": "error",
                "error": str(e),
                "success": False
            }
    
    async def _call_llm(
        self,
        user_message: str,
        language_code: str,
        prediction_label: Optional[str] = None,
        confidence_score: Optional[float] = None
    ) -> dict:
        """
        Call OpenAI LLM with domain restriction and language-aware prompts.
        
        Args:
            user_message: User message
            language_code: Language code
            prediction_label: MRI prediction
            confidence_score: Confidence score
            
        Returns:
            Dictionary with LLM response
        """
        try:
            # Build system prompt with domain restriction
            system_prompt = LanguageService.get_domain_prompt(language_code)
            
            # Add context if MRI prediction available
            if prediction_label and confidence_score:
                context = f"\n\nUser has uploaded an MRI scan. Prediction: {prediction_label} (Confidence: {confidence_score:.2%})"
                system_prompt += context
            
            # Add safety guidelines
            safety_guidelines = {
                "en": "\n\nIMPORTANT SAFETY RULES:\n1. Do NOT provide diagnoses\n2. Do NOT recommend medications or dosages\n3. Do NOT provide certainty about conditions\n4. Use phrases like 'may', 'could', 'might' instead of definitive statements\n5. Always recommend consulting healthcare professionals",
                "hi": "\n\nमहत्वपूर्ण सुरक्षा नियम:\n1. निदान न दें\n2. दवाओं या खुराक की सिफारिश न करें\n3. स्थितियों के बारे में निश्चितता न दें\n4. निश्चित कथन की बजाय 'हो सकता है', 'होता है' जैसे वाक्यांशों का उपयोग करें\n5. हमेशा स्वास्थ्यसेवा पेशेवरों से परामर्श की सिफारिश करें",
                "te": "\n\nఎముకతో కూడిన సూచనలు:\n1. నిర్ధారణ ఇవ్వకండి\n2. ఔషదాలు లేదా డోసేజ్‌ను సిఫారసు చేయవద్దు\n3. పరిస్థితుల గురించి నిశ్చయతను అందించవద్దు\n4. నిశ్చయమైన ప్రకటనల కు బదులుగా 'చేయవచ్చు', 'హోవచ్చు' వంటి పదబంధాలను ఉపయోగించండి\n5. ఎల్లప్పుడూ ఆరోగ్య సేవ నిపుణులను సంప్రదించమని సిఫారసు చేయండి"
            }
            
            system_prompt += safety_guidelines.get(language_code, safety_guidelines["en"])
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500,
                timeout=30
            )
            
            llm_response = response.choices[0].message.content.strip()
            logger.info("LLM response generated successfully")
            
            return {
                "response": llm_response,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            return {
                "response": None,
                "success": False,
                "error": str(e)
            }
    
    def _get_fallback_response(self, language_code: str) -> str:
        """Get fallback response when LLM is unavailable."""
        fallback_responses = {
            "en": "Brain imaging and tumor analysis require professional medical evaluation. Please consult with a neurology specialist or radiologist for accurate diagnosis and treatment planning.",
            "hi": "ब्रेन इमेजिंग और ट्यूमर विश्लेषण के लिए पेशेवर चिकित्सा मूल्यांकन की आवश्यकता है। सटीक निदान और उपचार योजना के लिए कृपया न्यूरोलॉजी विशेषज्ञ या रेडियोलॉजिस्ट से परामर्श लें।",
            "te": "బ్రెయిన్ ఇమేజింగ్ మరియు ట్యూమర్ విశ్లేషణకు వృత్తిపరమైన వైద్య మూల్యాంకనం అవసరం. ఖచ్చితమైన నిర్ధారణ మరియు చికిత్స ప్రణాళిక కోసం దయచేసి నిউరోలజీ విశేషజ్ఞ లేదా రేడియోలజిస్ట్‌ను సంప్రదించండి."
        }
        
        return fallback_responses.get(language_code, fallback_responses["en"])


# Initialize service
_chat_service = None

def get_chat_service() -> MultilingualChatService:
    """Get or create multilingual chat service."""
    global _chat_service
    if _chat_service is None:
        _chat_service = MultilingualChatService()
    return _chat_service
