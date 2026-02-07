"""
Rule-based chatbot logic for tumor-related queries.
Integrated with medical AI assistant guidelines and validation rules.
"""

from typing import Dict, List, Optional, Tuple
from app.utils.logger import get_logger
from app.core.medical_chatbot_rules import MedicalChatbotRules

logger = get_logger(__name__)


class Chatbot:
    """Rule-based chatbot for brain tumor information."""
    
    def __init__(self):
        """Initialize chatbot with knowledge base."""
        self.knowledge_base = {
            "tumor": [
                "Brain tumors are abnormal growths in the brain.",
                "They can be benign or malignant.",
                "Symptoms may include headaches, vision problems, and balance issues."
            ],
            "mri": [
                "MRI (Magnetic Resonance Imaging) is commonly used to detect brain tumors.",
                "MRI provides detailed images of the brain.",
                "It's a non-invasive imaging technique."
            ],
            "diagnosis": [
                "Brain tumor diagnosis requires professional medical evaluation.",
                "Imaging tests like MRI, CT, and PET scans are used.",
                "A biopsy may be necessary for definitive diagnosis."
            ],
            "treatment": [
                "Treatment options include surgery, radiation, and chemotherapy.",
                "Treatment depends on tumor type, size, and location.",
                "Consult with a medical professional for personalized treatment plans."
            ],
            "prognosis": [
                "Prognosis depends on tumor type, grade, and patient factors.",
                "Early detection improves treatment outcomes.",
                "Regular follow-up with medical professionals is important."
            ]
        }
    
    def generate_response(self, user_message: str, mri_data: Optional[Dict] = None) -> str:
        """
        Generate response based on user message with medical AI validation.
        
        Args:
            user_message: User's input message
            mri_data: Optional MRI prediction data for context
            
        Returns:
            Chatbot response (validated and enhanced with medical guidelines)
        """
        try:
            # Step 1: Check if question is relevant to brain tumors/MRI
            is_relevant, relevance_reason = MedicalChatbotRules.is_question_relevant(user_message)
            
            if not is_relevant:
                logger.warning(f"Off-topic question detected: {relevance_reason}")
                return MedicalChatbotRules.get_off_topic_redirect(user_message)
            
            # Step 2: Check if MRI data is needed but not provided (ONLY for specific analysis requests)
            asks_analysis = self._asks_for_mri_analysis(user_message)
            if asks_analysis and not mri_data:
                logger.info("MRI analysis requested without data")
                return MedicalChatbotRules.get_no_mri_data_message()
            
            # Step 3: Generate base response from knowledge base
            message_lower = user_message.lower()
            response = None
            
            # Check knowledge base for matches
            for key, responses in self.knowledge_base.items():
                if key in message_lower:
                    logger.info(f"Found match for key: {key}")
                    response = responses[0]
                    break
            
            # If no match found, use context-aware default
            if not response:
                response = self._generate_context_aware_response(user_message, mri_data)
            
            # Step 4: Validate and enhance response with medical AI rules
            enhanced_response, metadata = MedicalChatbotRules.validate_and_enhance_response(
                user_message, 
                response,
                mri_data
            )
            
            logger.info(f"Response validation metadata: {metadata}")
            
            # Step 5: Sanitize response for safety
            final_response = MedicalChatbotRules.sanitize_response(enhanced_response)
            
            return final_response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            error_response = "I encountered an error while processing your question. Please try again."
            return MedicalChatbotRules.add_medical_disclaimer(error_response)
    
    def is_medical_query(self, message: str) -> bool:
        """
        Check if message is medical-related.
        
        Args:
            message: User message
            
        Returns:
            True if message is medical-related
        """
        medical_keywords = [
            "tumor", "cancer", "brain", "mri", "ct", "scan",
            "diagnosis", "treatment", "surgery", "radiation",
            "symptom", "disease", "health"
        ]
        return any(keyword in message.lower() for keyword in medical_keywords)
    
    @staticmethod
    def _asks_for_mri_analysis(message: str) -> bool:
        """
        Check if user is asking for MRI analysis/interpretation.
        
        Args:
            message: User message
            
        Returns:
            True if asking for MRI analysis
        """
        analysis_keywords = [
            "analyze", "analyze my", "what does", "explain my", 
            "interpret", "what's in", "what is in", "findings",
            "what tumor", "what type", "looking at"
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in analysis_keywords)
    
    @staticmethod
    def _generate_context_aware_response(message: str, mri_data: Optional[Dict] = None) -> str:
        """
        Generate context-aware response when no knowledge base match found.
        
        Args:
            message: User message
            mri_data: Optional MRI prediction data
            
        Returns:
            Context-aware response
        """
        message_lower = message.lower()
        
        # If MRI data is available, provide context-specific response
        if mri_data:
            tumor_type = mri_data.get('tumor_type', 'tumor finding')
            confidence = mri_data.get('confidence', 0)
            
            response = (
                f"Based on your MRI analysis, the findings suggest a {tumor_type} "
                f"(confidence: {confidence:.1%}). "
                f"This is for informational purposes only. "
                f"Please consult with a qualified neurologist for professional diagnosis and treatment recommendations."
            )
            return response
        
        # Handle percentage/confidence questions even without MRI data
        if "percentage" in message_lower or "confidence" in message_lower or "score" in message_lower:
            return (
                "The confidence score indicates how likely the MRI findings match a specific tumor type based on our analysis. "
                "A higher percentage means stronger confidence in the prediction. "
                "However, only a qualified medical professional can provide definitive diagnosis."
            )
        
        # Handle general analysis questions
        if "analyze" in message_lower or "explain" in message_lower or "what does" in message_lower:
            return (
                "To provide detailed analysis of your MRI findings, please upload a brain MRI image. "
                "Once you do, I can explain what the analysis indicates about the tumor type and confidence level."
            )
        
        # Default context-aware response
        default_response = (
            "I'm a brain tumor information assistant specializing in MRI analysis. "
            "I can answer questions about brain tumors, MRI findings, symptoms, and general medical information. "
            "For specific analysis of your scan, please upload your MRI image. "
            "For medical decisions, please consult with a qualified healthcare professional."
        )
        return default_response
