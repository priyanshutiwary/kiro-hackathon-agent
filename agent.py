import asyncio
import logging
from dotenv import load_dotenv
import os
from time import perf_counter
from livekit import rtc, api
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
    Agent,        
    AgentSession, 
)
from livekit.agents.voice import room_io
from livekit.plugins import deepgram, openai, silero, noise_cancellation

# Load environment variables
load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("outbound-caller")

# 1. Define the Agent and Tools together (Version 1.0 Style)
class Assistant(Agent):
    def __init__(self, api_client: api.LiveKitAPI, room: rtc.Room, participant_identity: str) -> None:
        instructions = (
            "You are a scheduling assistant for a game development studio. Your interface with user will be voice. "
            "The customer's name is Kyle. His appointment is next Tuesday at 3pm. "
            "You will confirm the appointment details politely and professionally."
        )
        super().__init__(instructions=instructions)
        self.api = api_client
        self.room = room
        self.participant_identity = participant_identity

    @llm.function_tool # Use the new decorator directly in the Agent class
    async def end_call(self) -> None:
        """Called when the user wants to end the call"""
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

async def entrypoint(ctx: JobContext) -> None:
    logger.info(f"Connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    outbound_trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID")
    phone_number = ctx.job.metadata 
    user_identity = "phone_user"

    # Start dialing
    await ctx.api.sip.create_sip_participant(
        api.CreateSIPParticipantRequest(
            room_name=ctx.room.name,
            sip_trunk_id=outbound_trunk_id,
            sip_call_to=phone_number,
            participant_identity=user_identity,
        )
    )

    participant = await ctx.wait_for_participant(identity=user_identity)

    # 2. Create the Agent instance with required context
    agent = Assistant(api_client=ctx.api, room=ctx.room, participant_identity=user_identity)

    # 3. Initialize AgentSession (No fnc_ctx needed, it's automatic now)
    session = AgentSession(
        stt=deepgram.STT(model="nova-2-phonecall"),
        llm=openai.LLM(),
        tts=openai.TTS(),
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

    # Greet the user
    await session.generate_reply(instructions="Greet Kyle and confirm his appointment for next Tuesday.")

    # Keep the job alive until the participant leaves or timeout
    start_time = perf_counter()
    while perf_counter() - start_time < 600: 
        if participant.disconnect_reason:
            break
        await asyncio.sleep(1)

    ctx.shutdown()

def prewarm(proc: JobProcess) -> None:
    proc.userdata["vad"] = silero.VAD.load()

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="outbound-caller",
            prewarm_fnc=prewarm,
        )
    )