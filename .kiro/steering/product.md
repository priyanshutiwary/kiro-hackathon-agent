# Product Overview

> **📝 Documentation Maintenance**: When adding features, changing objectives, or updating user flows, update this file and run `@update-docs`.

## Product Purpose
A production-ready voice agent that makes outbound PSTN calls using LiveKit's real-time communication platform. This agent demonstrates how to build intelligent voice assistants that can initiate phone calls, conduct natural conversations, and perform automated tasks like appointment confirmations, reminders, and customer outreach.

## Target Users
**Primary Audience**: Developers and businesses building voice automation
- Contact centers automating appointment confirmations
- Healthcare providers sending appointment reminders
- Sales teams conducting outreach campaigns
- Customer service teams handling routine callbacks
- Developers learning voice AI integration

**User Needs**:
- Reliable outbound calling infrastructure
- Natural-sounding voice interactions
- Low-latency real-time communication
- Customizable conversation flows
- Easy integration with existing systems
- Production-ready voice pipeline

## Key Features

### Voice Pipeline
- **VAD (Voice Activity Detection)**: Silero VAD for detecting when users speak
- **STT (Speech-to-Text)**: Deepgram Nova-2 optimized for phone calls
- **LLM (Language Model)**: OpenAI GPT for intelligent conversation
- **TTS (Text-to-Speech)**: OpenAI TTS for natural voice synthesis
- **Noise Cancellation**: BVC (Background Voice Cancellation) for clear audio

### Outbound Calling
- LiveKit SIP Outbound Trunks integration
- Twilio SIP trunk support
- Configurable phone numbers for caller ID
- Automatic call dispatching
- Call control functions (end call, transfer, etc.)

### Agent Capabilities
- Appointment confirmation workflows
- Natural conversation handling
- Context-aware responses
- Callable tools for dynamic actions
- Graceful call termination
- Timeout handling (10-minute default)

### Developer Experience
- Simple CLI for local development
- Health check validation
- Model prewarming for faster cold starts
- Comprehensive logging with configurable levels
- Environment-based configuration
- Easy deployment to production

## Business Objectives
1. **Automation**: Reduce manual calling workload by 80%
2. **Scalability**: Handle 100+ concurrent calls per worker
3. **Quality**: Achieve >90% successful conversation completion
4. **Latency**: Maintain <500ms response time for natural flow
5. **Reliability**: 99.9% uptime for production deployments

## User Journey

### Initial Setup (30-60 minutes)
1. Clone repository and create virtual environment
2. Install Python dependencies
3. Configure environment variables (.env.local)
4. Set up Twilio account and phone number
5. Create Twilio SIP trunk with termination URI
6. Create LiveKit SIP Outbound Trunk
7. Run health check to validate configuration
8. (Optional) Pre-download models for faster startup

### Development Phase (1-3 days)
1. Customize agent instructions and personality
2. Add custom tools and functions
3. Modify conversation flows
4. Test with local development server
5. Adjust VAD/STT/TTS settings
6. Implement error handling
7. Add logging and monitoring

### Production Deployment (1-2 hours)
1. Deploy worker to cloud infrastructure
2. Configure production environment variables
3. Set up monitoring and alerts
4. Test outbound calling in production
5. Scale workers based on call volume

**Typical Workflow** (Post-Setup):
- Start worker: `python3 agent.py dev`
- Dispatch call: `lk dispatch create --new-room --agent-name outbound-caller --metadata "+1234567890"`
- Agent dials number: 5-10 seconds
- Conversation begins: Immediate after answer
- Agent completes task: 1-3 minutes
- Call ends gracefully: Automatic or user-initiated

## Success Criteria

**Technical Metrics**:
- Call connection success rate: >95%
- Average call latency: <500ms
- Speech recognition accuracy: >90%
- Voice synthesis quality: >4/5 rating
- Worker uptime: >99.9%

**Business Metrics**:
- Appointment confirmation rate: >80%
- Cost per call: <$0.10
- Calls handled per worker: 100+ concurrent
- Average call duration: 2-3 minutes
- Customer satisfaction: >4/5 rating

**Developer Metrics**:
- Setup time: <1 hour
- Time to first call: <30 minutes
- Documentation completeness: 100%
- Code maintainability: >8/10
- Community adoption: 500+ GitHub stars

**User Experience Metrics**:
- Natural conversation flow: >4/5 rating
- Call clarity: >4/5 rating
- Task completion rate: >85%
- Hang-up rate: <10%
- Callback requests: <5%
