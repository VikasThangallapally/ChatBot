"""
Multilingual chatbot endpoint with domain restriction and safety guardrails.
Supports Brain MRI and Brain Tumor questions only.
Auto-detects user language and responds accordingly.
"""

from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.multilingual_chat_service import get_chat_service
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Initialize multilingual chat service
chat_service = get_chat_service()


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Multilingual Brain MRI chatbot",
    description="Chat with the bot in your language. Supports English, Hindi, Telugu with auto-detection."
)
async def chat(request: ChatRequest):
    """
    Multilingual chatbot endpoint with safety guardrails.
    
    Features:
    - Auto-detects user language (English, Hindi, Telugu)
    - Domain restricted to Brain MRI and Brain Tumor topics only
    - Emergency symptom detection
    - Medical safety disclaimers
    - LLM-powered responses with fallback
    
    Args:
        request: Chat request with message and language
        
    Returns:
        ChatResponse: Bot response with language metadata
    """
    try:
        logger.info(f"Chat request received. Language: {request.language}, Message length: {len(request.message)}")
        
        # Generate multilingual response
        result = await chat_service.generate_response(
            user_message=request.message,
            language=request.language,
            prediction_label=request.prediction_label,
            confidence_score=request.confidence_score
        )
        
        # Build response
        response = ChatResponse(
            response=result["response"],
            language=result.get("language", "en"),
            source=result.get("source", "error"),
            is_unrelated=result.get("is_unrelated", False),
            is_medical_alert=result.get("is_medical_alert", False)
        )
        
        logger.info(f"Chat response completed. Source: {response.source}, Language: {response.language}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error during chat: {str(e)}", exc_info=True)
        
        # Determine language for error response
        error_lang = "en"
        try:
            if request.language != "auto":
                error_lang = request.language
        except:
            pass
        
        error_responses = {
            "en": "An error occurred while processing your request. Please try again.",
            "hi": "आपके अनुरोध को संसाधित करते समय एक त्रुटि हुई। कृपया पुनः प्रयास करें।",
            "te": "మీ అభ్యర్థనను ప్రక్రియ చేయడంలో ఒక లోపం సంభవించింది. దయచేసి మళ్లీ ప్రయత్నించండి."
        }
        
        return ChatResponse(
            response=error_responses.get(error_lang, error_responses["en"]),
            language=error_lang,
            source="error",
            is_unrelated=False,
            is_medical_alert=False
        )

