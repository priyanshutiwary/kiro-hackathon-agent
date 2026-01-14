"""
Service for managing call lifecycle and SIP operations.
"""
import json
import logging
from livekit import api
from livekit.agents import JobContext

logger = logging.getLogger("payment-agent.call-service")


class CallService:
    """Service to handle call setup and management operations."""
    
    @staticmethod
    async def setup_outbound_call(ctx: JobContext, outbound_trunk_id: str) -> str:
        """
        Set up an outbound SIP call and return the participant identity.
        
        Args:
            ctx: Job context containing room and metadata
            outbound_trunk_id: SIP trunk ID for outbound calls
            
        Returns:
            User identity for the call participant
        """
        # Extract phone number from metadata
        phone_number = ctx.job.metadata
        try:
            # If metadata is JSON, extract phone number
            if ctx.job.metadata.strip().startswith('{'):
                metadata_json = json.loads(ctx.job.metadata)
                phone_number = metadata_json.get('phone_number', ctx.job.metadata)
        except json.JSONDecodeError:
            # Use metadata as phone number directly
            pass
        
        user_identity = "phone_user"
        
        logger.info(f"Setting up outbound call:")
        logger.info(f"  - Room: {ctx.room.name}")
        logger.info(f"  - Phone number: {phone_number}")
        logger.info(f"  - Trunk ID: {outbound_trunk_id}")
        logger.info(f"  - User identity: {user_identity}")
        
        # Start dialing
        try:
            await ctx.api.sip.create_sip_participant(
                api.CreateSIPParticipantRequest(
                    room_name=ctx.room.name,
                    sip_trunk_id=outbound_trunk_id,
                    sip_call_to=phone_number,
                    participant_identity=user_identity,
                )
            )
            logger.info(f"✓ SIP participant creation request sent successfully")
        except Exception as e:
            logger.error(f"✗ Failed to create SIP participant: {e}")
            raise
        
        return user_identity