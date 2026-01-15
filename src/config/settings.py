"""
Configuration settings for the payment agent.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env.local")


class Settings:
    """Application settings and configuration."""
    
    # Call timeout in seconds (10 minutes)
    CALL_TIMEOUT = 600
    
    # SIP configuration
    SIP_OUTBOUND_TRUNK_ID = os.getenv("SIP_OUTBOUND_TRUNK_ID")
    
    # Agent configuration
    AGENT_NAME = "payment-reminder-agent"
    
    # Voice & Language Settings
    STT_MODEL = "nova-3"
    STT_LANGUAGE = "multi"  # Options: en-US, en-IN, en-GB, hi (Hindi), etc.
    
    TTS_VOICE = "shimmer"  # Options: alloy, echo, fable, onyx, nova, shimmer
    TTS_SPEED = 1.2      # Speed: 0.25 to 4.0 (1.0 is normal)
    
    # Default language (fallback)
    DEFAULT_LANGUAGE = "en"
    
    # Supported languages with cultural context and voice settings
    LANGUAGE_CONFIG = {
        "en": {
            "name": "English",
            "greeting": "Hello",
            "tone": "friendly and professional",
            "instruction": "Respond in clear, simple English",
            "cultural_note": "Be direct but polite",
            "voices": {
                "male": "a167e0f3-df7e-4d52-a9c3-f949145efdab",  # Cartesia male English
                "female": "9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"  # Cartesia female English
            }
        },
        "hi": {
            "name": "Hindi", 
            "greeting": "नमस्ते",
            "tone": "respectful and formal",
            "instruction": "केवल हिंदी में जवाब दें। कोई अंग्रेजी शब्द न मिलाएं",
            "cultural_note": "Use respectful language and formal address",
            "voices": {
                "male": "6303e5fb-a0a7-48f9-bb1a-dd42c216dc5d",  # Cartesia multilingual male
                "female": "95d51f79-c397-46f9-b49a-23763d3eaa2d"  # Cartesia multilingual female
            }
        },
        "hinglish": {
            "name": "Hinglish",
            "greeting": "Hello",
            "tone": "casual and friendly", 
            "instruction": "Mix Hindi and English naturally as Indians speak",
            "cultural_note": "Use familiar, conversational tone",
            "voices": {
                "male": "fd2ada67-c2d9-4afe-b474-6386b87d8fc3",  # Cartesia multilingual male
                "female": "95d51f79-c397-46f9-b49a-23763d3eaa2d"  # Cartesia multilingual female
            }
        }
    }
    
    # Default voice settings
    DEFAULT_VOICE_GENDER = "female"
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required settings are present."""
        if not cls.SIP_OUTBOUND_TRUNK_ID:
            raise ValueError("SIP_OUTBOUND_TRUNK_ID environment variable is required")


# Global settings instance
settings = Settings()