# Webhook Integration Implementation

## Overview

This document describes the webhook integration implemented for the Python payment reminder agent to report call status updates to the backend.

## Files Created/Modified

### New Files

1. **`src/services/webhook_client.py`**
   - Implements `WebhookClient` class for sending status updates
   - Handles HMAC-SHA256 authentication
   - Implements retry logic with exponential backoff (3 attempts)
   - Provides methods for all webhook events:
     - `send_call_answered(reminder_id)`
     - `send_call_completed(reminder_id, connected, duration, customer_response, notes)`
     - `send_call_failed(reminder_id, reason)`

### Modified Files

1. **`main.py`**
   - Added webhook client initialization
   - Extracts `reminder_id` from room metadata
   - Sends `call_answered` webhook when participant joins
   - Sends `call_failed` webhook on connection errors
   - Sends `call_completed` webhook when call ends
   - Tracks call duration for outcome reporting

2. **`src/config/settings.py`**
   - Added `WEBHOOK_URL` configuration
   - Added `WEBHOOK_SECRET` configuration

3. **`.env.example`**
   - Added webhook configuration documentation
   - Includes `WEBHOOK_URL` and `WEBHOOK_SECRET` placeholders

4. **`requirements.txt`**
   - Added `aiohttp>=3.9.0` dependency for HTTP requests

5. **`README.md`**
   - Added webhook configuration section
   - Documented environment variables
   - Explained webhook behavior and retry logic

## Requirements Satisfied

✅ **4.1**: Send webhook on 'call_answered' event  
✅ **4.2**: Send webhook on 'call_completed' event with outcome data  
✅ **4.3**: Send webhook on 'call_failed' event  
✅ **4.4**: Include reminder_id from room metadata  
✅ **4.5**: Include authentication credentials (HMAC signature)  
✅ **5.4**: Retry up to 3 times with exponential backoff  
✅ **5.5**: Log failures for manual investigation  

## Configuration

### Environment Variables

Add to `agent/.env.local`:

```bash
WEBHOOK_URL=https://yourdomain.com/api/webhooks/call-status
WEBHOOK_SECRET=your-secure-random-secret-key
```

**Important**: The `WEBHOOK_SECRET` must match the backend configuration exactly.

## Webhook Flow

### 1. Call Answered
```
Participant joins → send_call_answered(reminder_id)
Backend receives → Updates status to 'processing'
```

### 2. Call Completed
```
Call ends → Calculate duration → send_call_completed(...)
Backend receives → Updates status to 'completed' or 'pending'
Stores outcome data (duration, customer_response, notes)
```

### 3. Call Failed
```
Connection error → send_call_failed(reminder_id, reason)
Backend receives → Updates status to 'failed'
```

## Authentication

All webhook requests include an `X-Webhook-Signature` header containing an HMAC-SHA256 signature:

```python
signature = hmac.new(
    webhook_secret.encode('utf-8'),
    payload_json.encode('utf-8'),
    hashlib.sha256
).hexdigest()
```

The backend verifies this signature before processing the request.

## Retry Logic

The webhook client implements exponential backoff:

- **Attempt 1**: Immediate (0 seconds delay)
- **Attempt 2**: 2 seconds delay
- **Attempt 3**: 4 seconds delay

After 3 failed attempts, the error is logged with details for manual investigation.

## Error Handling

The implementation handles various error scenarios:

1. **Missing Configuration**: Logs warning, continues without webhooks
2. **No reminder_id**: Logs warning, skips webhook notifications
3. **Connection Timeout**: Sends `call_failed` webhook
4. **Setup Errors**: Sends `call_failed` webhook with error details
5. **Webhook Failures**: Retries with backoff, logs after exhaustion

## Testing

To test the webhook integration:

1. Configure both backend and agent with matching `WEBHOOK_SECRET`
2. Start the backend server
3. Start the Python agent: `python agent.py dev`
4. Dispatch a test call with reminder metadata
5. Monitor logs for webhook delivery confirmation

## Future Enhancements

The current implementation uses placeholder logic for determining `customer_response`. In production, you should:

1. Analyze the conversation transcript to determine actual customer response
2. Extract commitment details (payment date, amount, etc.)
3. Detect dispute reasons or concerns
4. Identify if customer already paid

This could be implemented by:
- Adding conversation analysis to the `PaymentAssistant` class
- Using LLM to classify customer responses
- Storing conversation state for outcome determination
