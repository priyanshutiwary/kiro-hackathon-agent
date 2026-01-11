# Technical Architecture

> **📝 Documentation Maintenance**: When making significant changes to tech stack, architecture, or security practices, update this file and run `@update-docs` to sync all documentation.

## Technology Stack

**Core**: Python 3.10+ • LiveKit Agents SDK 1.3.10+ • LiveKit RTC • LiveKit API

**Voice Pipeline**: Silero VAD 1.3.10+ • Deepgram STT 1.3.10+ • OpenAI LLM 1.3.10+ • OpenAI TTS 1.3.10+

**Plugins**: Turn Detector 1.3.10+ • Noise Cancellation 0.2.2+ • python-dotenv 1.0

**Infrastructure**: Twilio SIP Trunks • LiveKit Cloud • Docker (optional)

**Tools**: LiveKit CLI (`lk`) • Python venv • pip

## Architecture Overview

**Layers**: CLI Entry → Worker Process → Job Context → Agent Session → Voice Pipeline → SIP Trunk → PSTN

**Key Components**:
- **Worker**: Long-running process that handles job dispatches
- **Job Context**: Manages room connection and participant lifecycle
- **Agent**: Custom Assistant class with instructions and tools
- **Agent Session**: Orchestrates STT, LLM, TTS, and VAD
- **SIP Integration**: Bridges LiveKit rooms to PSTN via SIP trunks

**Data Flow**:
1. Dispatch command triggers job with phone number metadata
2. Worker creates room and connects
3. SIP participant created via LiveKit API
4. Agent session starts with voice pipeline
5. Audio flows: PSTN → SIP → LiveKit → Agent → TTS → SIP → PSTN
6. Agent processes speech, generates responses, controls call
7. Call ends via timeout, user action, or agent tool

## Development Environment

**Required**: Python 3.10+ • pip • LiveKit Cloud account • Twilio account • OpenAI API key • Deepgram API key

**Setup**:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env.local  # Edit with your keys
python3 agent.py healthcheck
python3 agent.py download-files  # Optional: prewarm models
```

**Key Environment Variables**: 
- `LIVEKIT_URL` • `LIVEKIT_API_KEY` • `LIVEKIT_API_SECRET`
- `OPENAI_API_KEY` • `DEEPGRAM_API_KEY`
- `SIP_OUTBOUND_TRUNK_ID`

**CLI Commands**:
- `python3 agent.py dev` - Run worker locally
- `python3 agent.py healthcheck` - Validate configuration
- `python3 agent.py download-files` - Pre-download models
- `python3 agent.py prewarm` - Alias for download-files
- `python3 agent.py --log-level DEBUG dev` - Debug mode

## Code Standards

**Python**: Type hints • Docstrings (Google style) • PEP 8 formatting • Async/await patterns

**Agent Design**: 
- Inherit from `Agent` base class
- Use `@llm.function_tool` decorator for callable tools
- Keep instructions clear and concise
- Handle errors gracefully in tools

**Naming**: 
- Classes (PascalCase) • Functions (snake_case) • Constants (UPPER_SNAKE_CASE)
- Private methods (prefix `_`) • Async functions (prefix `async`)

**Best Practices**: 
- Functions <50 lines • Clear variable names • Handle exceptions
- Log important events • Validate inputs • Use type hints
- Document complex logic • Keep agent instructions focused

**Logging**:
```python
logger = logging.getLogger("outbound-caller")
logger.info("Connection established")
logger.warning("Token refresh needed")
logger.error("Call failed", exc_info=True)
```

## Security

**API Keys**: Environment variables only • Never commit secrets • Use `.env.local` (gitignored)

**SIP Security**: 
- Credentials stored in separate JSON (not committed)
- Username/password authentication for SIP trunks
- Secure termination URIs (HTTPS/TLS)

**LiveKit Security**: 
- API key/secret for authentication
- Room-based isolation
- Participant identity validation
- Secure WebSocket connections (WSS)

**Best Practices**: 
- Rotate API keys regularly
- Use separate keys for dev/prod
- Validate phone numbers before dialing
- Implement rate limiting for production
- Monitor for suspicious activity
- Keep dependencies updated

## Voice Pipeline Configuration

**VAD (Voice Activity Detection)**:
```python
vad=silero.VAD.load()
```
- Detects speech start/end
- Reduces false triggers
- Optimized for phone audio

**STT (Speech-to-Text)**:
```python
stt=deepgram.STT(model="nova-2-phonecall")
```
- Nova-2 optimized for phone calls
- Low latency streaming
- High accuracy for conversational speech

**LLM (Language Model)**:
```python
llm=openai.LLM()
```
- GPT-4 or GPT-3.5-turbo
- Streaming responses
- Function calling support

**TTS (Text-to-Speech)**:
```python
tts=openai.TTS()
```
- Natural voice synthesis
- Low latency streaming
- Multiple voice options

**Noise Cancellation**:
```python
room_options=room_io.RoomOptions(
    audio_input=room_io.AudioInputOptions(
        noise_cancellation=noise_cancellation.BVC(),
    ),
)
```
- Background Voice Cancellation
- Improves speech recognition
- Reduces ambient noise

## Deployment

**Docker** (Optional):
```bash
docker build -t outbound-caller .
docker run --env-file .env.local outbound-caller
```

**Production Considerations**:
- Use process manager (systemd, supervisor)
- Configure log rotation
- Set up health check monitoring
- Scale workers based on call volume
- Use production-grade SIP provider
- Implement retry logic for failed calls
- Monitor costs (API usage, SIP minutes)

**Environment Variables** (Production):
- Use secrets management (AWS Secrets Manager, etc.)
- Separate dev/staging/prod configurations
- Validate all required vars on startup
- Use secure credential storage for SIP

## Performance Optimization

**Model Prewarming**:
```bash
python3 agent.py download-files
```
- Downloads VAD model to cache
- Reduces cold start time
- Run before production deployment

**Concurrency**:
- Each worker handles multiple jobs
- Jobs run in separate rooms
- Scale workers horizontally
- Monitor CPU/memory usage

**Latency Optimization**:
- Use streaming for STT/TTS
- Minimize LLM prompt length
- Cache common responses
- Optimize tool execution time
- Use regional LiveKit servers

**Cost Optimization**:
- Choose appropriate LLM model
- Implement conversation timeouts
- Monitor API usage
- Use efficient prompts
- Batch operations where possible
