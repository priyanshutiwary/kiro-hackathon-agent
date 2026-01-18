"""
Webhook client for reporting call status updates to the backend.

Requirements:
- 4.1: Send webhook on call_answered event
- 4.2: Send webhook on call_completed event with outcome data
- 4.3: Send webhook on call_failed event
- 4.4: Include reminder_id from room metadata
- 4.5: Include authentication credentials
- 5.4: Retry up to 3 times with exponential backoff
- 5.5: Log failures for manual investigation
"""
import asyncio
import hashlib
import hmac
import json
import logging
from typing import Optional, Dict, Any
import aiohttp

logger = logging.getLogger("payment-agent.webhook")


class WebhookClient:
    """Client for sending call status updates to the backend webhook."""
    
    def __init__(self, webhook_url: str, webhook_secret: str):
        """
        Initialize webhook client.
        
        Args:
            webhook_url: The URL of the webhook endpoint
            webhook_secret: Secret key for HMAC authentication
        """
        self.webhook_url = webhook_url
        self.webhook_secret = webhook_secret
        self.max_retries = 3
        
    def _generate_signature(self, payload: str) -> str:
        """
        Generate HMAC signature for webhook authentication.
        
        Args:
            payload: JSON string of the request payload
            
        Returns:
            Hex-encoded HMAC signature
        """
        return hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    async def _send_with_retry(
        self,
        payload: Dict[str, Any],
        attempt: int = 1
    ) -> bool:
        """
        Send webhook request with exponential backoff retry logic.
        
        Requirement 5.4: Retry up to 3 times with exponential backoff
        - Attempt 1: Immediate
        - Attempt 2: 2 seconds delay
        - Attempt 3: 4 seconds delay
        
        Args:
            payload: Request payload dictionary
            attempt: Current attempt number (1-indexed)
            
        Returns:
            True if successful, False otherwise
        """
        # Convert payload to JSON string
        payload_json = json.dumps(payload)
        
        # Generate HMAC signature (Requirement 4.5)
        signature = self._generate_signature(payload_json)
        
        headers = {
            'Content-Type': 'application/json',
            'X-Webhook-Signature': signature
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    data=payload_json,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        logger.info(
                            f"Webhook sent successfully for reminder {payload.get('reminder_id')} "
                            f"(event: {payload.get('event_type')})"
                        )
                        return True
                    else:
                        response_text = await response.text()
                        logger.warning(
                            f"Webhook failed with status {response.status}: {response_text} "
                            f"(attempt {attempt}/{self.max_retries})"
                        )
                        
        except asyncio.TimeoutError:
            logger.warning(
                f"Webhook request timed out (attempt {attempt}/{self.max_retries})"
            )
        except aiohttp.ClientError as e:
            logger.warning(
                f"Webhook request failed: {e} (attempt {attempt}/{self.max_retries})"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error sending webhook: {e} (attempt {attempt}/{self.max_retries})"
            )
        
        # Retry logic with exponential backoff
        if attempt < self.max_retries:
            # Calculate delay: 2^(attempt-1) seconds (0, 2, 4)
            delay = 2 ** (attempt - 1) if attempt > 1 else 0
            if delay > 0:
                logger.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            
            return await self._send_with_retry(payload, attempt + 1)
        
        # All retries exhausted (Requirement 5.5)
        logger.error(
            f"All webhook retry attempts exhausted for reminder {payload.get('reminder_id')} "
            f"(event: {payload.get('event_type')}). Manual investigation required."
        )
        return False
    
    async def send_call_answered(self, reminder_id: str) -> bool:
        """
        Send webhook notification when call is answered.
        
        Requirement 4.1: Send webhook on call_answered event
        Requirement 4.4: Include reminder_id from room metadata
        
        Args:
            reminder_id: The reminder ID from room metadata
            
        Returns:
            True if webhook sent successfully, False otherwise
        """
        payload = {
            'reminder_id': reminder_id,
            'event_type': 'call_answered'
        }
        
        logger.info(f"Sending call_answered webhook for reminder {reminder_id}")
        return await self._send_with_retry(payload)
    
    async def send_call_completed(
        self,
        reminder_id: str,
        connected: bool,
        duration: int,
        customer_response: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Send webhook notification when call is completed.
        
        Requirement 4.2: Send webhook on call_completed event with outcome data
        Requirement 4.4: Include reminder_id from room metadata
        
        Args:
            reminder_id: The reminder ID from room metadata
            connected: Whether the call was successfully connected
            duration: Call duration in seconds
            customer_response: Customer response type (will_pay_today, already_paid, dispute, no_answer)
            notes: Optional notes from the agent
            
        Returns:
            True if webhook sent successfully, False otherwise
        """
        payload = {
            'reminder_id': reminder_id,
            'event_type': 'call_completed',
            'outcome': {
                'connected': connected,
                'duration': duration,
                'customer_response': customer_response,
            }
        }
        
        if notes:
            payload['outcome']['notes'] = notes
        
        logger.info(
            f"Sending call_completed webhook for reminder {reminder_id} "
            f"(response: {customer_response}, duration: {duration}s)"
        )
        return await self._send_with_retry(payload)
    
    async def send_call_failed(
        self,
        reminder_id: str,
        reason: Optional[str] = None
    ) -> bool:
        """
        Send webhook notification when call fails.
        
        Requirement 4.3: Send webhook on call_failed event
        Requirement 4.4: Include reminder_id from room metadata
        
        Args:
            reminder_id: The reminder ID from room metadata
            reason: Optional reason for call failure
            
        Returns:
            True if webhook sent successfully, False otherwise
        """
        payload = {
            'reminder_id': reminder_id,
            'event_type': 'call_failed',
            'outcome': {
                'connected': False,
                'duration': 0,
                'customer_response': 'no_answer',
            }
        }
        
        if reason:
            payload['outcome']['notes'] = reason
        
        logger.info(f"Sending call_failed webhook for reminder {reminder_id}")
        return await self._send_with_retry(payload)
