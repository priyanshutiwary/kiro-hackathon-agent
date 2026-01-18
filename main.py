"""
Main entry point for the payment reminder agent.
"""
import asyncio
import logging
from time import perf_counter
from dotenv import load_dotenv
from livekit.plugins import cartesia

# Load environment variables first
load_dotenv(dotenv_path=".env.local")

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    AgentSession,
)
from livekit.agents.voice import room_io
from livekit.plugins import deepgram, openai, silero, noise_cancellation

from src.config.settings import settings
from src.utils.context_parser import parse_payment_context
from src.agents.payment_assistant import PaymentAssistant
from src.services.call_service import CallService
from src.services.greeting_service import GreetingService
from src.services.webhook_client import WebhookClient

logger = logging.getLogger("payment-agent")


def get_voice_config(payment_context):
    """Get voice configuration based on language and gender."""
    language = payment_context.language
    gender = payment_context.voice_gender
    
    # Get language config, fallback to default if not found
    lang_config = settings.LANGUAGE_CONFIG.get(language, settings.LANGUAGE_CONFIG[settings.DEFAULT_LANGUAGE])
    
    # Get voice ID for the specified gender, fallback to female if not found
    voice_id = lang_config['voices'].get(gender, lang_config['voices']['female'])
    
    logger.info(f"Selected voice: language={language}, gender={gender}, voice_id={voice_id}")
    
    return voice_id


async def entrypoint(ctx: JobContext) -> None:
    """Main entry point for payment reminder calls."""
    logger.info("=" * 60)
    logger.info("NEW JOB RECEIVED")
    logger.info(f"Room: {ctx.room.name}")
    logger.info(f"Job ID: {ctx.job.id if hasattr(ctx.job, 'id') else 'N/A'}")
    logger.info(f"Metadata: {ctx.job.metadata}")
    logger.info("=" * 60)
    
    # Extract reminder_id from room name (Requirement 4.4)
    # Room name format: payment-reminder-{reminderId}-{timestamp}-{random}
    # Note: reminderId is a UUID with dashes (e.g., e93d3d67-1234-5678-9abc-def012345678)
    reminder_id = None
    webhook_client = None
    try:
        room_name = ctx.room.name
        logger.info(f"Parsing room name: {room_name}")
        
        if room_name.startswith('payment-reminder-'):
            # Remove the 'payment-reminder-' prefix
            remainder = room_name[len('payment-reminder-'):]
            
            # UUID format: 8-4-4-4-12 characters (with dashes)
            # We need to extract the first 36 characters (UUID with dashes)
            # Format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
            if len(remainder) >= 36:
                # Extract the UUID (first 36 characters)
                reminder_id = remainder[:36]
                logger.info(f"✓ Extracted reminder_id from room name: {reminder_id}")
            else:
                logger.warning(f"Room name format unexpected, remainder too short: {remainder}")
        else:
            logger.warning(f"Room name doesn't start with 'payment-reminder-': {room_name}")
        
        if reminder_id:
            # Initialize webhook client if configuration is available
            webhook_url = settings.WEBHOOK_URL if hasattr(settings, 'WEBHOOK_URL') else None
            webhook_secret = settings.WEBHOOK_SECRET if hasattr(settings, 'WEBHOOK_SECRET') else None
            
            if webhook_url and webhook_secret:
                webhook_client = WebhookClient(webhook_url, webhook_secret)
                logger.info(f"✓ Webhook client initialized for reminder {reminder_id}")
            else:
                logger.warning("Webhook configuration not found. Status updates will not be sent.")
                logger.warning(f"WEBHOOK_URL present: {webhook_url is not None}")
                logger.warning(f"WEBHOOK_SECRET present: {webhook_secret is not None}")
        else:
            logger.warning("No reminder_id extracted from room name. Webhook notifications will be skipped.")
    except Exception as e:
        logger.error(f"Error extracting reminder_id from room name: {e}", exc_info=True)
    
    logger.info(f"Connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info("✓ Connected to room successfully")

    # Validate configuration
    settings.validate()
    
    # Parse payment context from metadata
    payment_context = parse_payment_context(ctx.job.metadata)
    logger.info(f"Parsed payment context: customer={payment_context.customer_name}, "
                f"invoice={payment_context.invoice_number}, amount={payment_context.amount_due}")
    
    # Set up outbound call
    call_connected = False
    try:
        user_identity = await CallService.setup_outbound_call(ctx, settings.SIP_OUTBOUND_TRUNK_ID)
        logger.info(f"Waiting for participant {user_identity} to join...")
        
        # Wait for participant with timeout
        participant = await asyncio.wait_for(
            ctx.wait_for_participant(identity=user_identity),
            timeout=30.0  # 30 second timeout
        )
        logger.info(f"Participant {user_identity} joined successfully")
        call_connected = True
        
        # Send call_answered webhook (Requirement 4.1)
        if webhook_client and reminder_id:
            await webhook_client.send_call_answered(reminder_id)
        
    except asyncio.TimeoutError:
        logger.error(f"Timeout waiting for participant {user_identity} to join. Call may have failed.")
        
        # Send call_failed webhook (Requirement 4.3)
        if webhook_client and reminder_id:
            await webhook_client.send_call_failed(reminder_id, "Timeout waiting for participant to join")
        
        ctx.shutdown()
        return
    except Exception as e:
        logger.error(f"Error setting up call: {e}")
        
        # Send call_failed webhook (Requirement 4.3)
        if webhook_client and reminder_id:
            await webhook_client.send_call_failed(reminder_id, f"Error setting up call: {str(e)}")
        
        ctx.shutdown()
        return

    # Create the payment assistant agent
    agent = PaymentAssistant(
        api_client=ctx.api, 
        room=ctx.room, 
        participant_identity=user_identity, 
        payment_context=payment_context
    )

    # Get dynamic voice configuration based on language and gender
    voice_id = get_voice_config(payment_context)
    
    # Initialize agent session with voice capabilities
    session = AgentSession(
        stt=deepgram.STT(
            model=settings.STT_MODEL, 
            language=settings.STT_LANGUAGE,
            endpointing_ms=500,  # Increased from default 25ms to allow natural pauses
            interim_results=True,  # Keep interim results for better responsiveness
        ),
        llm=openai.LLM(),
        tts=cartesia.TTS(
            voice=voice_id,  # Dynamic voice based on language and gender
            model="sonic-3",  # Use multilingual model
            language=payment_context.language,  # Set language for TTS
            speed=1.0,
        ),
        vad=silero.VAD.load(),
    )

    # Start the session
    await session.start(
        room=ctx.room,
        agent=agent,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
            ),
        ),
    )

    # Generate and deliver professional greeting
    greeting_instructions = GreetingService.generate_greeting_instructions(payment_context)
    await session.generate_reply(instructions=greeting_instructions)

    # Keep the job alive until the participant leaves or timeout
    start_time = perf_counter()
    call_duration = 0
    call_was_answered = False
    
    # Wait for participant to disconnect or timeout
    while perf_counter() - start_time < settings.CALL_TIMEOUT: 
        if participant.disconnect_reason:
            call_duration = int(perf_counter() - start_time)
            logger.info(f"Participant disconnected. Reason: {participant.disconnect_reason}, Duration: {call_duration}s")
            break
        await asyncio.sleep(1)
    
    # Calculate final call duration
    if call_duration == 0:
        call_duration = int(perf_counter() - start_time)
    
    # Determine if call was actually answered based on duration
    # If call lasted more than 5 seconds, assume customer answered
    # Otherwise, it was likely no answer, busy, or rejected
    call_was_answered = call_duration > 5
    
    logger.info(f"Call ended. Duration: {call_duration}s, Answered: {call_was_answered}")
    
    # Send call_completed webhook (Requirement 4.2)
    if webhook_client and reminder_id and call_connected:
        if not call_was_answered:
            # Call was not answered - likely no answer, busy, or rejected
            logger.info(f"Call was not answered (duration: {call_duration}s)")
            await webhook_client.send_call_completed(
                reminder_id=reminder_id,
                connected=False,
                duration=call_duration,
                customer_response='no_answer',
                notes=f"Call not answered - duration {call_duration}s"
            )
        else:
            # Call was answered - determine response based on conversation
            # This is a simplified version - in production, analyze the conversation
            customer_response = 'no_answer'  # Default
            notes = None
            
            # If call lasted more than 10 seconds, assume some interaction occurred
            if call_duration > 10:
                customer_response = 'will_pay_today'  # Placeholder - should be determined from conversation
                notes = f"Call completed after {call_duration} seconds"
            
            await webhook_client.send_call_completed(
                reminder_id=reminder_id,
                connected=True,
                duration=call_duration,
                customer_response=customer_response,
                notes=notes
            )

    ctx.shutdown()


def prewarm(proc: JobProcess) -> None:
    """Prewarm function to load models before job execution."""
    proc.userdata["vad"] = silero.VAD.load()


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name=settings.AGENT_NAME,
            prewarm_fnc=prewarm,
        )
    )