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
    try:
        user_identity = await CallService.setup_outbound_call(ctx, settings.SIP_OUTBOUND_TRUNK_ID)
        logger.info(f"Waiting for participant {user_identity} to join...")
        
        # Wait for participant with timeout
        participant = await asyncio.wait_for(
            ctx.wait_for_participant(identity=user_identity),
            timeout=30.0  # 30 second timeout
        )
        logger.info(f"Participant {user_identity} joined successfully")
    except asyncio.TimeoutError:
        logger.error(f"Timeout waiting for participant {user_identity} to join. Call may have failed.")
        ctx.shutdown()
        return
    except Exception as e:
        logger.error(f"Error setting up call: {e}")
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
        stt=deepgram.STT(model=settings.STT_MODEL, language=settings.STT_LANGUAGE),
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
    while perf_counter() - start_time < settings.CALL_TIMEOUT: 
        if participant.disconnect_reason:
            break
        await asyncio.sleep(1)

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