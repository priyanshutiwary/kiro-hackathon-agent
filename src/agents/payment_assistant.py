"""
Payment reminder assistant agent with professional communication capabilities.
"""
import logging
from livekit import rtc, api
from livekit.agents import Agent, llm
from src.models.payment_context import PaymentContext

logger = logging.getLogger("payment-agent.assistant")


class PaymentAssistant(Agent):
    """Professional payment reminder agent with enhanced communication standards."""
    
    def __init__(self, api_client: api.LiveKitAPI, room: rtc.Room, 
                 participant_identity: str, payment_context: PaymentContext) -> None:
        # Create comprehensive payment reminder instructions using context
        amount_text = f"${payment_context.amount_due:.2f}" if payment_context.amount_due else "the outstanding amount"
        
        instructions = self._build_instructions(payment_context, amount_text)
        super().__init__(instructions=instructions)
        
        self.api = api_client
        self.room = room
        self.participant_identity = participant_identity
        self.payment_context = payment_context

    def _build_instructions(self, payment_context: PaymentContext, amount_text: str) -> str:
        """Build language-aware instructions using single prompt with parameters."""
        from src.config.settings import settings
        
        # Get language configuration
        language = payment_context.language
        lang_config = settings.LANGUAGE_CONFIG.get(language, settings.LANGUAGE_CONFIG[settings.DEFAULT_LANGUAGE])
        
        return (
            f"You are a {payment_context.voice_gender} agent calling on behalf of {payment_context.company_name} about a payment. "
            f"{lang_config['instruction']}. "
            f"Use a {lang_config['tone']} tone. {lang_config['cultural_note']}. "
            f"Speak as a {payment_context.voice_gender} would naturally speak. "
            f"\n\nCUSTOMER INFO:"
            f"\n- Name: {payment_context.customer_name}"
            f"\n- Invoice: {payment_context.invoice_number}"
            f"\n- Amount: {amount_text}"
            f"\n- Due: {payment_context.due_date}"
            f"\n- Language: {lang_config['name']}"
            f"\n- Your Voice: {payment_context.voice_gender}"
            f"\n\nHOW TO COMMUNICATE:"
            f"\n- Be friendly and direct - get to the point quickly"
            f"\n- Keep responses SHORT - 1-2 sentences max per turn"
            f"\n- Sound natural, not scripted"
            f"\n- Match their energy - if casual, be casual. If brief, be brief"
            f"\n\nOPENING:"
            f"\nThe call has already been opened for you with a scripted greeting that mentions "
            f"{payment_context.company_name}, invoice {payment_context.invoice_number} and {amount_text}. "
            f"Do NOT greet again or repeat that introduction - respond directly to what the customer says."
            f"\n\nRESPONSE PATTERNS:"
            f"\n- Already paid? → 'Great! Can you share confirmation details?'"
            f"\n- Need more time? → 'Sure, when works for you?'"
            f"\n- Disputing it? → 'Got it. What's the issue?'"
            f"\n- Confused? → 'Let me clarify...' then explain briefly"
            f"\n- Upset? → Stay calm, acknowledge, focus on solving"
            f"\n- Busy? → 'Should I call back later?'"
            f"\n\nKEY RULES:"
            f"\n- {lang_config['instruction']}"
            f"\n- Keep it SHORT - don't ramble"
            f"\n- Listen more than you talk"
            f"\n- If they want to end call, say 'Thanks, have a good day' and use end_call"
            f"\n- Aim for 1-2 minute calls maximum"
            f"\n- Be polite but not overly formal"
        )

    @llm.function_tool
    async def end_call(self) -> None:
        """
        Called when the customer wants to end the call or when the conversation should be terminated.
        Handles graceful disconnection by removing the participant from the room.
        This satisfies requirements 3.1 and 3.3 for proper call management.
        """
        logger.info(f"Ending the call for {self.participant_identity}")
        try:
            await self.api.room.remove_participant(
                api.RoomParticipantIdentity(
                    room=self.room.name, 
                    identity=self.participant_identity
                )
            )
        except Exception as e:
            logger.info(f"Error while ending call: {e}")