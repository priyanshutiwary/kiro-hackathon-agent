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
    
    # Webhook configuration (Requirement 4.5)
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
    
    # Voice & Language Settings
    STT_MODEL = "nova-3"
    STT_LANGUAGE = "multi"  # Options: en-US, en-IN, en-GB, hi (Hindi), etc.
    # Keep Deepgram endpointing short; the turn detector model decides when the user is done
    STT_ENDPOINTING_MS = 25

    # Smaller model = much lower time-to-first-token (plugin default is gpt-4.1)
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")

    # Latency tuning (seconds)
    # Silence to wait after the turn detector thinks the user is done
    MIN_ENDPOINTING_DELAY = 0.3
    # Upper bound when the turn detector thinks the user is mid-sentence
    MAX_ENDPOINTING_DELAY = 2.0
    # Start the LLM on interim transcripts before the turn is final
    PREEMPTIVE_GENERATION = True

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
            # Scripted opening spoken via session.say() so the first words don't wait on the LLM
            "opening": (
                "Hello {customer_name}, I'm calling from {company_name} about invoice "
                "{invoice_number} for {amount}, which was due {due_date}. "
                "Is there anything holding up the payment?"
            ),
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
            # {speaking} is "रही" (female) / "रहा" (male)
            "opening": (
                "नमस्ते {customer_name} जी, मैं {company_name} की तरफ़ से इनवॉइस {invoice_number} "
                "के भुगतान के बारे में बात कर {speaking} हूँ, जिसकी राशि {amount} है। "
                "क्या भुगतान में कोई दिक्कत आ रही है?"
            ),
            "speaking": {"female": "रही", "male": "रहा"},
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
            "opening": (
                "Hello {customer_name}, main {company_name} se bol {speaking} hoon, invoice "
                "{invoice_number} ke payment ke baare mein, jo {amount} ka hai. "
                "Payment mein koi issue aa raha hai kya?"
            ),
            "speaking": {"female": "rahi", "male": "raha"},
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