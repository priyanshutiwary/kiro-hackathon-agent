"""
Service for generating professional greeting messages for payment calls.
"""
from src.models.payment_context import PaymentContext


class GreetingService:
    """Service to generate professional and courteous greeting messages."""
    
    @staticmethod
    def generate_greeting_instructions(payment_context: PaymentContext) -> str:
        """
        Generate language-aware greeting instructions.
        
        Args:
            payment_context: Payment context containing customer and invoice details
            
        Returns:
            Language-specific greeting instructions for the agent
        """
        from src.config.settings import settings
        
        amount_text = f"${payment_context.amount_due:.2f}" if payment_context.amount_due else "the outstanding amount"
        
        # Get language configuration
        language = payment_context.language
        lang_config = settings.LANGUAGE_CONFIG.get(language, settings.LANGUAGE_CONFIG[settings.DEFAULT_LANGUAGE])
        
        return (
            f"Start the call naturally in {lang_config['name']}: "
            f"Use '{lang_config['greeting']} {payment_context.customer_name}', then say you're calling from {payment_context.company_name} "
            f"about invoice {payment_context.invoice_number} for {amount_text} that was due {payment_context.due_date}. "
            f"Then ask if they have questions or what's holding up the payment. "
            f"Remember: {lang_config['instruction']}. Use a {lang_config['tone']} tone. "
            f"Keep it brief and natural - don't sound scripted."
        )