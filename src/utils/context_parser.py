"""
Utility functions for parsing payment context from job metadata.
"""
import json
import logging
from src.models.payment_context import PaymentContext

logger = logging.getLogger("payment-agent.context-parser")


def parse_payment_context(metadata: str) -> PaymentContext:
    """
    Parse payment context from job metadata.
    
    Args:
        metadata: JSON string or plain string containing payment context
        
    Returns:
        PaymentContext object with extracted or default values
    """
    try:
        # Try to parse as JSON first
        if metadata.strip().startswith('{'):
            context_data = json.loads(metadata)
            return PaymentContext(
                customer_name=context_data.get('customer_name'),
                invoice_number=context_data.get('invoice_number'),
                amount_due=context_data.get('amount_due'),
                due_date=context_data.get('due_date'),
                company_name=context_data.get('company_name'),
                language=context_data.get('language', 'en'),  # Default to English
                voice_gender=context_data.get('voice_gender', 'female')  # Default to female
            )
        else:
            # If not JSON, treat as phone number (legacy behavior)
            logger.info(f"Metadata appears to be phone number: {metadata}")
            return PaymentContext()
            
    except (json.JSONDecodeError, AttributeError) as e:
        logger.warning(f"Failed to parse payment context from metadata: {e}")
        logger.info(f"Using default payment context values")
        return PaymentContext()