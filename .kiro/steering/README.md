# Kiro Steering Documents

This directory contains steering documents that guide Kiro's understanding of the LiveKit Outbound Caller Voice Agent project.

## Documents

### product.md
Defines the product vision, target users, key features, and success criteria. Use this to understand:
- What the voice agent does and why
- Who uses it and their needs
- Business objectives and metrics
- User journey from setup to production

### tech.md
Describes the technical architecture, technology stack, and development practices. Use this to understand:
- Voice pipeline components (VAD, STT, LLM, TTS)
- LiveKit and SIP integration
- Code standards and best practices
- Security and deployment considerations

### structure.md
Documents the project structure, file organization, and naming conventions. Use this to understand:
- Directory layout and file purposes
- Code organization patterns
- Configuration management
- Development workflow

## Usage with Kiro

These steering documents are automatically included in Kiro's context when working on this project. They help Kiro:
- Maintain consistent code style and architecture
- Make decisions aligned with project goals
- Understand the voice agent's purpose and design
- Follow established patterns and conventions

## Updating Documents

When making significant changes to the project:
1. Update the relevant steering document(s)
2. Run `@update-docs` to sync all documentation
3. Commit the changes with a descriptive message

## Quick Reference

**Voice Pipeline**: Silero VAD → Deepgram STT → OpenAI LLM → OpenAI TTS  
**SIP Integration**: Twilio SIP Trunk → LiveKit SIP Outbound → PSTN  
**Agent Pattern**: Class-based with `@llm.function_tool` decorators  
**CLI Commands**: `dev`, `healthcheck`, `download-files`, `prewarm`  
**Key Files**: `agent.py`, `.env.local`, `outbound-trunk.json`
