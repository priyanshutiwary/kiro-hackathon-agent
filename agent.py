"""
Simple entry point that uses the main payment agent implementation.
This file serves as a wrapper to run the payment reminder agent.
"""
# Load environment variables FIRST before any other imports
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")

from main import entrypoint, prewarm
from livekit.agents import WorkerOptions, cli
from src.config.settings import settings


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name=settings.AGENT_NAME,
            prewarm_fnc=prewarm,
        )
    )
