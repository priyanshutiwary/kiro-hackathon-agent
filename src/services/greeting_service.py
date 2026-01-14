"""
Service for generating professional greeting messages for payment calls.
"""
from src.models.payment_context import PaymentContext


class GreetingService:
    """Service to generate professional and courteous greeting messages."""
    
    @staticmethod
    def generate_greeting_instructions(payment_context: PaymentContext) -> str:
        """
        Generate comprehensive greeting instructions with professional tone.
        
        Args:
            payment_context: Payment context containing customer and invoice details
            
        Returns:
            Formatted greeting instructions for the agent
        """
        amount_text = f"${payment_context.amount_due:.2f}" if payment_context.amount_due else "the outstanding amount"
        
        # Step 1: Greet customer by name from context with enhanced professionalism
        greeting_message = (
            f"Good day, {payment_context.customer_name}. This is a courteous payment reminder call from {payment_context.company_name}. "
            f"I hope I'm reaching you at a convenient time."
        )
        
        # Step 2: Mention specific invoice number and amount with polite language
        invoice_details = (
            f"I'm calling to discuss invoice number {payment_context.invoice_number} "
            f"for {amount_text}. I wanted to bring this to your attention respectfully."
        )
        
        # Step 3: Explain payment due date clearly with understanding tone
        due_date_explanation = (
            f"According to our records, this payment was due on {payment_context.due_date}."
        )
        
        # Step 4: Ask if customer has questions with helpful approach
        question_prompt = (
            f"I'd be happy to help clarify any questions you might have about this invoice, "
            f"or if you'd like to discuss payment options that might work for your situation."
        )
        
        # Combine all parts into comprehensive greeting instructions with professional tone
        return (
            f"Begin the call with this professional and respectful approach: "
            f"1. {greeting_message} "
            f"2. {invoice_details} "
            f"3. {due_date_explanation} "
            f"4. {question_prompt} "
            f"Deliver this naturally as a warm, professional conversation. Use a courteous tone throughout. "
            f"Be patient and understanding. Wait for their response and listen carefully to address their needs."
        )