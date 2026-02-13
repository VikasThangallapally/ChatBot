"""
Language detection and management service.
Detects user language and manages multilingual responses.
"""

from langdetect import detect, DetectorFactory
from typing import Literal
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "auto": "Auto-detect"
}

# Language code mapping
LANG_MAP = {
    "english": "en",
    "hindi": "hi",
    "telugu": "te",
    "en": "en",
    "hi": "hi",
    "te": "te"
}

# Different language prompts for domain restriction
DOMAIN_RESTRICTION_PROMPTS = {
    "en": "You are a medical AI assistant specialized in Brain MRI and Brain Tumor information only. You must ONLY answer questions related to brain MRI scans, brain tumors, and brain imaging. For ANY question outside this domain, you must respond with EXACTLY: 'I can only answer brain MRI and brain tumor related questions.' Do not add any additional text or explanation.",
    
    "hi": "आप एक चिकित्सा AI सहायक हैं जो केवल ब्रेन MRI और ब्रेन ट्यूमर जानकारी के लिए विशेषज्ञ हैं। आप केवल ब्रेन MRI स्कैन, ब्रेन ट्यूमर, और ब्रेन इमेजिंग से संबंधित प्रश्नों का उत्तर दे सकते हैं। इस डोमेन के बाहर किसी भी प्रश्न के लिए, आपको बिल्कुल इसी तरह जवाब देना चाहिए: 'मैं केवल ब्रेन MRI और ब्रेन ट्यूमर से संबंधित प्रश्नों का उत्तर दे सकता हूँ।' कोई अतिरिक्त पाठ या व्याख्या न जोड़ें।",
    
    "te": "మీరు బ్రెయిన్ MRI మరియు బ్రెయిన్ ట్యూమర్ సమాచారం కోసం మాత్రమే నిపుణులైన వైద్య AI సహాయకుడు. మీరు బ్రెయిన్ MRI స్కాన్‌లు, బ్రెయిన్ ట్యూమర్‌లు మరియు బ్రెయిన్ ఇమేజింగ్‌కు సంబంధించిన ప్రశ్నలకు మాత్రమే సమాధానం ఇవ్వగలరు. ఈ డోమైన్‌కు వెలుపల ఏదైనా ప్రశ్నకు, మీరు ఖచ్చితంగా ఇలా సమాధానం చెప్పుకోవాలి: 'నేను బ్రెయిన్ MRI మరియు బ్రెయిన్ ట్యూమర్ సంబంధిత ప్రశ్నలకు మాత్రమే సమాధానం ఇవ్వగలను.' అదనపు పాఠం లేదా వివరణ జోడించవద్దు।"
}

# Medical disclaimer prompts in different languages
MEDICAL_DISCLAIMER_PROMPTS = {
    "en": "\n\n⚠️ MEDICAL DISCLAIMER: This is educational information only. It is NOT a diagnosis or medical advice. Do NOT use this as a substitute for professional medical consultation. Always consult with a qualified healthcare provider for medical concerns.",
    
    "hi": "\n\n⚠️ चिकित्सा अस्वीकरण: यह केवल शैक्षणिक जानकारी है। यह निदान या चिकित्सा सलाह नहीं है। इसे पेशेवर चिकित्सा परामर्श के स्थान पर न उपयोग करें। चिकित्सा संबंधी चिंताओं के लिए हमेशा एक योग्य स्वास्थ्यसेवा प्रदाता से परामर्श लें।",
    
    "te": "\n\n⚠️ వైద్య నిరాకరణ: ఇది విద్యా సమాచారం మాత్రమే. ఇది నిర్ధారణ లేదా వైద్య సలహా కాదు. దీనిని వృత్తిపరమైన వైద్య సంప్రামాణం యొక్క ప్రత్యామ్నాయంగా ఉపయోగించవద్దు. వైద్య సంబంధిత ఆందోళనల కోసం ఎల్లప్పుడూ నిపుణ జట్టు సదస్యలను సంప్రదించండి."
}

# Emergency symptoms in different languages
EMERGENCY_SYMPTOMS = {
    "en": ["seizure", "fainting", "faint", "unconscious", "severe headache", "headache", "vomiting", "vision loss", "blind", "stroke", "paralysis", "lose consciousness"],
    "hi": ["दौरा", "बेहोश", "गंभीर सिरदर्द", "उल्टी", "दृष्टि हानि", "लकवा", "चेतना खोना"],
    "te": ["మూర్ఛ", "తీవ్ర తలనొప్పి", "వాంతులు", "దృష్టి నష్టం", "పక్షవात", "స్పృహ కోల్పోవడం"]
}

EMERGENCY_RESPONSE = {
    "en": "Please seek emergency medical care immediately. This is a serious condition that requires urgent medical attention.",
    "hi": "कृपया तुरंत आपातकालीन चिकित्सा सेवा लें। यह एक गंभीर स्थिति है जिसके लिए तत्काल चिकित्सा ध्यान की आवश्यकता है।",
    "te": "దయచేసి వెంటనე అత్యవసర వైద్య సేవలను పొందండి. ఇది తక్షణ వైద్య శ్రద్ధ అవసరమైన తీవ్ర స్థితి."
}

UNRELATED_RESPONSE = {
    "en": "I can only answer brain MRI and brain tumor related questions.",
    "hi": "मैं केवल ब्रेन MRI और ब्रेन ट्यूमर से संबंधित प्रश्नों का उत्तर दे सकता हूँ।",
    "te": "నేను బ్రెయిన్ MRI మరియు బ్రెయిన్ ట్యూమర్ సంబంధిత ప్రశ్నలకు మాత్రమే సమాధానం ఇవ్వగలను."
}


class LanguageService:
    """Handles language detection and multilingual responses."""
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect language from text.
        
        Args:
            text: Text to detect language from
            
        Returns:
            Language code (en, hi, te)
        """
        try:
            detected = detect(text)
            
            # Map detected language to supported language
            if detected in ["en"]:
                return "en"
            elif detected in ["hi"]:
                return "hi"
            elif detected in ["te"]:
                return "te"
            else:
                # Default to English if not supported
                logger.warning(f"Detected language {detected} not supported, defaulting to English")
                return "en"
        except Exception as e:
            logger.warning(f"Language detection failed: {str(e)}, defaulting to English")
            return "en"
    
    @staticmethod
    def get_language_code(language: str) -> str:
        """
        Get normalized language code.
        
        Args:
            language: Language name or code
            
        Returns:
            Normalized language code
        """
        lang_lower = language.lower().strip()
        return LANG_MAP.get(lang_lower, "en")
    
    @staticmethod
    def get_domain_prompt(language_code: str) -> str:
        """Get domain restriction prompt for language."""
        return DOMAIN_RESTRICTION_PROMPTS.get(language_code, DOMAIN_RESTRICTION_PROMPTS["en"])
    
    @staticmethod
    def get_medical_disclaimer(language_code: str) -> str:
        """Get medical disclaimer for language."""
        return MEDICAL_DISCLAIMER_PROMPTS.get(language_code, MEDICAL_DISCLAIMER_PROMPTS["en"])
    
    @staticmethod
    def get_unrelated_response(language_code: str) -> str:
        """Get unrelated question response for language."""
        return UNRELATED_RESPONSE.get(language_code, UNRELATED_RESPONSE["en"])
    
    @staticmethod
    def get_emergency_response(language_code: str) -> str:
        """Get emergency response for language."""
        return EMERGENCY_RESPONSE.get(language_code, EMERGENCY_RESPONSE["en"])
    
    @staticmethod
    def check_emergency_symptoms(text: str, language_code: str) -> bool:
        """
        Check if text mentions emergency symptoms.
        
        Args:
            text: User message
            language_code: Language code
            
        Returns:
            True if emergency symptoms detected
        """
        text_lower = text.lower()
        symptoms = EMERGENCY_SYMPTOMS.get(language_code, EMERGENCY_SYMPTOMS["en"])
        
        for symptom in symptoms:
            if symptom in text_lower:
                return True
        
        return False
    
    @staticmethod
    def is_brain_related(text: str, language_code: str = "en") -> bool:
        """
        Check if question is brain/MRI related.
        Uses keyword matching as a quick filter.
        
        Args:
            text: User message
            language_code: Language code
            
        Returns:
            True if likely brain-related
        """
        brain_keywords = {
            "en": ["brain", "mri", "tumor", "scan", "imaging", "neural", "glioma", "glioblastoma", "meningioma", "neurology", "neuro", "ct", "fmri", "neurological", "cerebral", "skull", "cortex", "white matter", "grey matter", "lesion"],
            "hi": ["मस्तिष्क", "mri", "ट्यूमर", "स्कैन", "इमेजिंग", "तंत्रिका", "न्यूरोलॉजी", "अनुभव"],
            "te": ["మెదడు", "mri", "종양", "స్కాన్", "ఇమేజింగ్", "నాడీ", "న్యూరోలజీ"]
        }
        
        text_lower = text.lower()
        keywords = brain_keywords.get(language_code, brain_keywords["en"])
        
        for keyword in keywords:
            if keyword in text_lower:
                return True
        
        return False
