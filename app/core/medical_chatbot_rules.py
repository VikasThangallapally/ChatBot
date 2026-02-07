"""
Medical Chatbot Rules Engine

Enforces medical AI assistant guidelines:
- Context validation
- Question relevance checking
- Prohibited content detection
- Medical disclaimer management
- Off-topic handling
"""

import re
from typing import Dict, Tuple, Optional, List
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MedicalChatbotRules:
    """Enforces medical AI assistant rules and guidelines."""
    
    # Relevant topics for medical AI
    RELEVANT_TOPICS = {
        "brain tumors", "tumor types", "glioma", "meningioma", "pituitary", 
        "mri", "scan", "imaging", "findings", "diagnosis", "prognosis",
        "symptoms", "treatment", "surgery", "radiation", "chemotherapy",
        "neurology", "neurologist", "brain", "cancer", "biopsy",
        "medical", "health", "patient", "clinical", "outcome", "result",
        "analyze", "explain", "percentage", "confidence", "prediction",
        "what", "how", "why", "can", "will", "should"
    }
    
    # Prohibited actions (can explain but not recommend)
    PROHIBITED_PATTERNS = {
        "diagnose|diagnosed|diagnosis": "diagnosis",
        "treat|treatment|therapy|medication|medicine|drug": "treatment",
        "prescribe|prescription": "medication prescription",
        "surgery|surgical|operate|operation": "surgery recommendation",
        "dose|dosage": "medication dosage",
        "cure|cured": "cure claim"
    }
    
    # Off-topic redirect keywords
    OFF_TOPIC_KEYWORDS = {
        "recipe", "cooking", "sports", "movie", "music", "weather",
        "politics", "finance", "car", "house", "vacation", "relationship",
        "homework", "coding", "coding problem", "programming"
    }
    
    # Medical disclaimer templates
    MEDICAL_DISCLAIMERS = {
        "general": "⚠️ Medical Disclaimer: This information is educational only and not a substitute for professional medical advice. Always consult with a qualified healthcare provider.",
        "diagnosis": "⚠️ Important: Only a qualified medical professional can provide diagnosis. Please see a neurologist or physician for definitive assessment.",
        "treatment": "⚠️ Important: Treatment decisions must be made with your healthcare team. Do not make treatment decisions based solely on this information.",
        "urgent": "🚨 If experiencing severe symptoms, seek emergency medical care immediately."
    }
    
    @staticmethod
    def is_question_relevant(question: str) -> Tuple[bool, str]:
        """
        Check if question is relevant to brain tumors and MRI analysis.
        Uses flexible logic that accepts medical context questions.
        
        Args:
            question: User's question
            
        Returns:
            (is_relevant: bool, reason: str)
        """
        question_lower = question.lower().strip()
        
        # Empty questions are not relevant
        if not question_lower or len(question_lower) < 3:
            return False, "Question is too short or empty"
        
        # Check for STRONG off-topic keywords (definitive rejection)
        strong_off_topic = {
            "recipe", "cooking", "football", "basketball", "baseball",
            "movie review", "music playlist", "weather forecast",
            "stock price", "crypto", "bitcoin", "car review"
        }
        for keyword in strong_off_topic:
            if keyword in question_lower:
                return False, f"This question about '{keyword}' is outside the scope"
        
        # Accept if contains strong medical/brain keywords
        strong_medical_keywords = {
            "brain", "tumor", "mri", "scan", "glioma", "meningioma", 
            "pituitary", "cancer", "diagnosis", "treatment", "surgical",
            "neurologist", "neurology", "imaging"
        }
        if any(keyword in question_lower for keyword in strong_medical_keywords):
            return True, "Question contains medical keywords"
        
        # Accept general medical context questions if they contain inquiry words + medical terms
        inquiry_words = {"what", "how", "why", "when", "where", "which", "can", "will", "does", "is", "are"}
        has_inquiry = any(word in question_lower for word in inquiry_words)
        
        # Accept questions that ask about analysis/findings
        analysis_words = {"analyze", "explain", "meaning", "indicate", "suggest", "mean", "result", "finding", "percentage", "confidence", "score"}
        has_analysis = any(word in question_lower for word in analysis_words)
        
        # If it's an inquiry with analysis intent, likely medical context
        if has_inquiry and has_analysis:
            return True, "Question appears to be about analysis or findings"
        
        # Check for relevant medical topics more flexibly
        found_relevant = any(
            topic in question_lower 
            for topic in MedicalChatbotRules.RELEVANT_TOPICS
        )
        
        if found_relevant:
            return True, "Question is relevant"
        
        # If nothing matched, accept it as potentially medical context
        # (better to answer and include disclaimer than reject valid questions)
        if has_inquiry or len(question_lower.split()) >= 3:
            return True, "Accepting as potential medical inquiry (fallback)"
        
        return False, "Question doesn't appear to be medical-related"
    
    @staticmethod
    def check_prohibited_content(response: str) -> Tuple[bool, Optional[str]]:
        """
        Check if response contains prohibited medical advice.
        
        Args:
            response: Generated response text
            
        Returns:
            (is_safe: bool, violation_type: Optional[str])
        """
        response_lower = response.lower()
        
        for pattern, violation_type in MedicalChatbotRules.PROHIBITED_PATTERNS.items():
            # Check for strong directive language
            if re.search(f"(you should|you must|you need to|i recommend|take|take this) {pattern}", response_lower):
                return False, f"Directive {violation_type} detected"
            
            # Check for prescription-like statements
            if re.search(f"(prescribed|prescription for|medication for) {pattern}", response_lower):
                return False, f"Prescription {violation_type} detected"
        
        return True, None
    
    @staticmethod
    def add_medical_disclaimer(response: str, disclaimer_type: str = "general") -> str:
        """
        Add appropriate medical disclaimer to response.
        
        Args:
            response: Original response text
            disclaimer_type: Type of disclaimer to add
            
        Returns:
            Response with disclaimer appended
        """
        disclaimer = MedicalChatbotRules.MEDICAL_DISCLAIMERS.get(
            disclaimer_type, 
            MedicalChatbotRules.MEDICAL_DISCLAIMERS["general"]
        )
        
        # Check if disclaimer already present
        if "⚠️" in response or "🚨" in response:
            return response
        
        return f"{response}\n\n{disclaimer}"
    
    @staticmethod
    def get_off_topic_redirect(question: str) -> str:
        """
        Generate helpful off-topic redirect message.
        
        Args:
            question: User's off-topic question
            
        Returns:
            Friendly redirect message
        """
        return (
            "I appreciate your question, but I'm specifically designed to help with brain MRI analysis "
            "and brain tumor information. Could you ask something related to brain tumors, MRI findings, "
            "or medical imaging? If you have an MRI scan, please upload it and I can help explain the results!"
        )
    
    @staticmethod
    def get_no_mri_data_message() -> str:
        """
        Message when user asks for analysis but hasn't uploaded MRI.
        
        Returns:
            Guidance message
        """
        return (
            "I'd be happy to help explain your MRI findings! However, I don't see any MRI prediction data yet. "
            "Please upload a brain MRI image first, and then ask your question. "
            "I'll provide context-specific explanations based on your scan results."
        )
    
    @staticmethod
    def sanitize_response(response: str) -> str:
        """
        Sanitize response to ensure it meets medical AI standards.
        
        Args:
            response: Generated response
            
        Returns:
            Sanitized response
        """
        # Remove aggressive language
        response = re.sub(r"\byou must\b", "you may want to", response, flags=re.IGNORECASE)
        response = re.sub(r"\byou should\b", "it may be helpful to", response, flags=re.IGNORECASE)
        response = re.sub(r"\byou need to\b", "you may consider", response, flags=re.IGNORECASE)
        
        # Remove diagnostic certainty
        response = re.sub(r"\bwill definitely\b", "may", response, flags=re.IGNORECASE)
        response = re.sub(r"\bwill certainly\b", "may", response, flags=re.IGNORECASE)
        response = re.sub(r"\byou have\b", "findings may suggest", response, flags=re.IGNORECASE)
        
        # Remove treatment recommendations
        response = re.sub(r"\bI recommend\b", "doctors often consider", response, flags=re.IGNORECASE)
        response = re.sub(r"\bI suggest\b", "some options may include", response, flags=re.IGNORECASE)
        
        return response.strip()
    
    @staticmethod
    def validate_and_enhance_response(
        question: str,
        response: str,
        mri_data: Optional[Dict] = None
    ) -> Tuple[str, Dict[str, any]]:
        """
        Validate and enhance response based on medical AI rules.
        
        Args:
            question: User's question
            response: Generated response
            mri_data: Optional MRI prediction data for context
            
        Returns:
            (enhanced_response: str, metadata: Dict)
        """
        metadata = {
            "question_relevant": False,
            "response_safe": True,
            "disclaimer_added": False,
            "issues": []
        }
        
        # Check question relevance
        is_relevant, relevance_reason = MedicalChatbotRules.is_question_relevant(question)
        metadata["question_relevant"] = is_relevant
        
        if not is_relevant:
            logger.warning(f"Off-topic question detected: {relevance_reason}")
            metadata["issues"].append(f"Off-topic: {relevance_reason}")
            return MedicalChatbotRules.get_off_topic_redirect(question), metadata
        
        # Check for prohibited content
        is_safe, violation = MedicalChatbotRules.check_prohibited_content(response)
        metadata["response_safe"] = is_safe
        
        if not is_safe:
            logger.warning(f"Prohibited content detected: {violation}")
            metadata["issues"].append(f"Safety violation: {violation}")
            # Sanitize response
            response = MedicalChatbotRules.sanitize_response(response)
        
        # Add medical disclaimer
        if not any(d in response for d in ["⚠️", "🚨"]):
            response = MedicalChatbotRules.add_medical_disclaimer(response)
            metadata["disclaimer_added"] = True
        
        # Sanitize response for general safety
        response = MedicalChatbotRules.sanitize_response(response)
        
        logger.info(f"Response validated. Issues: {metadata['issues']}")
        
        return response, metadata


def validate_medical_response(question: str, response: str, mri_data: Optional[Dict] = None) -> str:
    """
    Simple wrapper function to validate and enhance medical response.
    
    Args:
        question: User's question
        response: Generated response
        mri_data: Optional MRI prediction data
        
    Returns:
        Enhanced response
    """
    enhanced_response, _ = MedicalChatbotRules.validate_and_enhance_response(
        question, response, mri_data
    )
    return enhanced_response
