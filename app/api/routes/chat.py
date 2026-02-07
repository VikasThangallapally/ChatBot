"""
Chatbot endpoint for interactive explanation generation.
Integrates GPT-based intelligence with fallback to rule-based responses.
"""

from fastapi import APIRouter
from app.services.explanation import ExplanationService
from app.services.gpt_service import get_gpt_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.chatbot import Chatbot
from app.core.disclaimer import get_disclaimer
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Initialize chatbot
chatbot = Chatbot()
gpt_service = get_gpt_service()


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Interactive chatbot for tumor explanations",
    description="Chat with the bot to get human-readable explanations powered by GPT"
)
async def chat(request: ChatRequest):
    """
    Interactive chatbot endpoint for explanations.
    Supports GPT-based responses with fallback to rule-based chatbot.
    
    Args:
        request: Chat request with user message and optional MRI prediction context
        
    Returns:
        ChatResponse: Bot response with explanation, source, and disclaimer
    """
    try:
        # Try GPT-based response first if service is available
        response_text = None
        explanation = None
        source = "fallback"
        
        if gpt_service.is_available():
            logger.info(f"GPT service available, generating response for: {request.message[:50]}...")
            
            # Call GPT service with prediction context
            gpt_result = await gpt_service.generate_response(
                user_question=request.message,
                prediction_label=request.prediction_label,
                confidence_score=request.confidence_score
            )
            
            if gpt_result["source"] == "gpt":
                response_text = gpt_result["reply"]
                source = "gpt"
                logger.info(f"GPT response generated successfully")
            else:
                logger.warning(f"GPT generation failed: {gpt_result.get('error', 'Unknown error')}")
        else:
            logger.info("GPT service not available, using fallback chatbot")
        
        # Fall back to rule-based chatbot if GPT failed
        if response_text is None:
            logger.info("Falling back to rule-based chatbot")
            # Pass MRI data to chatbot for context-aware responses
            mri_context = None
            if request.prediction_label and request.confidence_score:
                mri_context = {
                    "tumor_type": request.prediction_label,
                    "confidence": request.confidence_score
                }
            response_text = chatbot.generate_response(
                request.message,
                mri_data=mri_context
            )
            source = "fallback"
        
        # Generate explanation if needed
        explanation_service = ExplanationService()
        explanation = explanation_service.explain_response(response_text)
        
        logger.info(f"Chat response completed. Source: {source}, Message: {request.message[:50]}")
        
        return ChatResponse(
            response=response_text,
            explanation=explanation,
            source=source,
            disclaimer=get_disclaimer()
        )
        
    except Exception as e:
        logger.error(f"Error during chat: {str(e)}")
        return ChatResponse(
            response="An error occurred while processing your request. Please try again with a different question.",
            explanation="If this error persists, please consult with a medical professional.",
            source="error",
            disclaimer=get_disclaimer()
        )
