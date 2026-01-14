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
    
    # STT/TTS Models
    STT_MODEL = "nova-2-phonecall"
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required settings are present."""
        if not cls.SIP_OUTBOUND_TRUNK_ID:
            raise ValueError("SIP_OUTBOUND_TRUNK_ID environment variable is required")


# Global settings instance
settings = Settings()