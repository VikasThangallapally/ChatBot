"""
GPT-based Intelligence Service for Brain Tumor Chatbot.

Integrates OpenAI's GPT API to provide intelligent, context-aware responses
about MRI prediction results. Includes strict system prompts for safety and
error handling with fallback to rule-based responses.
"""

import os
from typing import Dict, Any, Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Strict system prompt for medical safety
SYSTEM_PROMPT = """You are a medical AI assistant specializing in brain MRI analysis and brain tumor information.

CORE RESPONSIBILITIES:
- Answer ONLY questions related to brain tumors, MRI findings, and general medical information
- Base explanations on provided MRI prediction data when available
- If no MRI prediction data provided, ask user to upload an MRI scan first
- Intelligently infer intent from spelling mistakes or unclear wording
- Interpret ambiguous questions with the most likely medical context
- Use clear, calm, easy-to-understand language
- Avoid repeating generic textbook definitions unless explicitly asked

SAFETY AND ETHICAL RULES (STRICT):
1. NEVER diagnose diseases - only explain what MRI findings may indicate
2. NEVER recommend specific medications or treatments
3. NEVER claim certainty about medical outcomes or prognosis
4. ALWAYS include a medical disclaimer in every response
5. ALWAYS encourage consulting a qualified medical professional
6. Keep responses concise (2-3 paragraphs maximum)
7. Use simple, non-technical language where possible
8. If unsure about anything, recommend professional medical consultation

CONTEXT-AWARE BEHAVIOR:
- When MRI prediction data is provided, reference it specifically in explanations
- Tailor responses to the user's tumor type/finding when available
- Use patient-friendly terminology while remaining medically accurate
- Acknowledge emotional concerns with empathy

OFF-TOPIC HANDLING:
- If question is outside brain tumor/MRI context, gently redirect user back to relevant topics
- Remain helpful but stay within scope of medical AI assistant

Your responses should be informative, empathetic, evidence-based, and always directed toward professional medical guidance."""


class GPTService:
    """Service for generating intelligent responses using OpenAI GPT."""
    
    def __init__(self):
        """Initialize GPT service with API key from environment."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.client = None
        self.available = False
        
        # Initialize OpenAI client if API key is available
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                self.available = True
                logger.info("GPT service initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {str(e)}")
                self.available = False
        else:
            logger.warning("OPENAI_API_KEY not found in environment. GPT service disabled.")
            self.available = False
    
    async def generate_response(
        self,
        user_question: str,
        prediction_label: Optional[str] = None,
        confidence_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Generate a GPT-based response to a user question with MRI context.
        
        Args:
            user_question: The user's natural language question
            prediction_label: The predicted tumor type (e.g., "Glioma Tumor")
            confidence_score: The model's confidence (0.0-1.0)
            
        Returns:
            Dictionary with:
            - reply: The generated response
            - source: 'gpt' if successful, 'error' if failed
            - model: Model name used
        """
        try:
            if not self.available or not self.client:
                logger.warning("GPT service not available, cannot generate response")
                return {
                    "reply": None,
                    "source": "unavailable",
                    "model": None,
                    "error": "GPT service not configured"
                }
            
            # Build context message with prediction information
            context = self._build_context(user_question, prediction_label, confidence_score)
            
            logger.info(f"Generating GPT response for: {user_question[:60]}...")
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,  # Balanced between creativity and consistency
                max_tokens=500,   # Limit response length
                timeout=10        # 10 second timeout
            )
            
            # Extract response
            reply = response.choices[0].message.content.strip()
            
            logger.info(f"GPT response generated successfully ({len(reply)} chars)")
            
            return {
                "reply": reply,
                "source": "gpt",
                "model": self.model,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
            }
            
        except Exception as e:
            logger.error(f"GPT API error: {str(e)}")
            return {
                "reply": None,
                "source": "error",
                "model": self.model,
                "error": str(e)
            }
    
    def _build_context(
        self,
        user_question: str,
        prediction_label: Optional[str] = None,
        confidence_score: Optional[float] = None
    ) -> str:
        """
        Build the context message to send to GPT.
        
        Args:
            user_question: User's question
            prediction_label: Predicted tumor type
            confidence_score: Confidence percentage
            
        Returns:
            Formatted context string
        """
        context = f"User Question: {user_question}\n\n"
        
        # Add MRI prediction context if available
        if prediction_label and confidence_score is not None:
            context += f"MRI Analysis Context:\n"
            context += f"- Predicted Finding: {prediction_label}\n"
            context += f"- Model Confidence: {confidence_score*100:.1f}%\n\n"
            context += f"Based on this MRI finding, please answer the user's question educationally and safely."
        else:
            context += "Please answer the user's question about brain MRI findings educationally and safely."
        
        return context
    
    def is_available(self) -> bool:
        """Check if GPT service is available."""
        return self.available


# Global service instance
_gpt_service = None


def get_gpt_service() -> GPTService:
    """Get or initialize the global GPT service instance."""
    global _gpt_service
    if _gpt_service is None:
        _gpt_service = GPTService()
    return _gpt_service
