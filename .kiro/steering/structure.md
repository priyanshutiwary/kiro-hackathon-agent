# Project Structure

> **📝 Documentation Maintenance**: When adding new directories, changing file organization, or updating conventions, update this file and run `@update-docs`.

## Directory Layout

```
LiveKit-Outbound-Caller-Voice-Agent/
├── agent.py                    # Main agent implementation
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── .env.local                 # Local environment (gitignored)
├── .gitignore                 # Git ignore rules
├── .dockerignore              # Docker ignore rules
├── Dockerfile                 # Container configuration
├── README.md                  # Project documentation
├── livekit.toml              # LiveKit CLI configuration
├── outbound-trunk-example.json # SIP trunk template
├── outbound-trunk.json        # SIP trunk config (gitignored)
├── venv/                      # Python virtual environment (gitignored)
├── .git/                      # Git repository
└── .kiro/                     # Kiro CLI configuration
    ├── steering/              # Development guidelines
    │   ├── product.md        # Product overview
    │   ├── tech.md           # Technical architecture
    │   └── structure.md      # This file
    └── prompts/               # Custom Kiro commands (optional)
```

## File Descriptions

**Core Files**:
- `agent.py` - Main entry point with Agent class, tools, and entrypoint function
- `requirements.txt` - Python package dependencies with version constraints
- `.env.local` - Environment variables (API keys, credentials)
- `livekit.toml` - LiveKit CLI configuration for project settings

**Configuration**:
- `outbound-trunk.json` - SIP trunk credentials (DO NOT COMMIT)
- `outbound-trunk-example.json` - Template for SIP trunk configuration
- `Dockerfile` - Container image for production deployment
- `.dockerignore` - Files to exclude from Docker build

**Documentation**:
- `README.md` - Setup instructions, features, and usage guide
- `.kiro/steering/*.md` - Development guidelines and architecture docs

## Naming Conventions

**Python Files**: snake_case (`agent.py`, `utils.py`)

**Classes**: PascalCase (`Assistant`, `VoiceAgent`)

**Functions**: snake_case (`entrypoint`, `end_call`, `validate_required_env`)

**Constants**: UPPER_SNAKE_CASE (`REQUIRED_ENV_VARS`, `MAX_CALL_DURATION`)

**Private Functions**: Prefix with underscore (`_configure_logging`, `_validate_phone`)

**Async Functions**: Use `async def` keyword, name normally (`async def entrypoint`)

## Code Organization

**agent.py Structure**:
```python
# 1. Imports
import asyncio
import logging
from livekit.agents import Agent, AgentSession
# ... other imports

# 2. Configuration
load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("outbound-caller")

# 3. Helper Functions
def _configure_logging(level: str) -> None:
    """Configure logging with format"""
    pass

def validate_required_env() -> None:
    """Validate environment variables"""
    pass

# 4. Agent Class
class Assistant(Agent):
    """Main agent with instructions and tools"""
    
    def __init__(self, api_client, room, participant_identity):
        instructions = "..."
        super().__init__(instructions=instructions)
        # Store context
    
    @llm.function_tool
    async def end_call(self) -> None:
        """Tool for ending calls"""
        pass
    
    @llm.function_tool
    async def other_tool(self, param: str) -> str:
        """Other callable tools"""
        pass

# 5. Entrypoint Function
async def entrypoint(ctx: JobContext) -> None:
    """Main job handler"""
    # Connect to room
    # Create SIP participant
    # Initialize agent and session
    # Start conversation
    # Wait for completion
    pass

# 6. Prewarm Function
def prewarm(proc: JobProcess) -> None:
    """Pre-download models"""
    pass

# 7. CLI Entry Point
if __name__ == "__main__":
    cli.run_app(WorkerOptions(...))
```

## Import Conventions

**Standard Library First**:
```python
import asyncio
import logging
import os
from time import perf_counter
```

**Third-Party Packages**:
```python
from dotenv import load_dotenv
from livekit import rtc, api
from livekit.agents import Agent, AgentSession
from livekit.plugins import deepgram, openai, silero
```

**Import Order**: Standard library → Third-party → Local modules

## Environment Variables

**Required Variables**:
```bash
# LiveKit Configuration
LIVEKIT_URL="wss://your-project.livekit.cloud"
LIVEKIT_API_KEY="APIxxxxx"
LIVEKIT_API_SECRET="xxxxxx"

# AI Services
OPENAI_API_KEY="sk-proj-xxxxx"
DEEPGRAM_API_KEY="xxxxx"

# SIP Configuration
SIP_OUTBOUND_TRUNK_ID="ST_xxxxx"
```

**File Locations**:
- `.env.example` - Template with placeholder values
- `.env.local` - Actual values (gitignored, used by code)
- Never commit `.env.local` or any file with real credentials

## Configuration Files

**livekit.toml**:
```toml
[project]
name = "outbound-caller"
```

**outbound-trunk.json** (gitignored):
```json
{
  "name": "My Twilio Trunk",
  "address": "sip:your-trunk.pstn.twilio.com",
  "numbers": ["+1234567890"],
  "auth_username": "username",
  "auth_password": "password"
}
```

**Dockerfile**:
- Multi-stage build for smaller images
- Python 3.10+ base image
- Install dependencies from requirements.txt
- Copy agent.py and configuration
- Set entrypoint to run agent

## Git Ignore Rules

**Always Ignore**:
- `venv/` - Virtual environment
- `.env.local` - Environment variables
- `outbound-trunk.json` - SIP credentials
- `__pycache__/` - Python bytecode
- `*.pyc` - Compiled Python files
- `.DS_Store` - macOS metadata
- `*.log` - Log files

**Commit These**:
- `.env.example` - Template
- `outbound-trunk-example.json` - Template
- `requirements.txt` - Dependencies
- `agent.py` - Source code
- `README.md` - Documentation
- `.gitignore` - Ignore rules

## Development Workflow

**Initial Setup**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env.local
# Edit .env.local with your keys
```

**Daily Development**:
```bash
source venv/bin/activate
python3 agent.py dev
# In another terminal:
lk dispatch create --new-room --agent-name outbound-caller --metadata "+1234567890"
```

**Adding Features**:
1. Add new tool methods to `Assistant` class
2. Use `@llm.function_tool` decorator
3. Update agent instructions if needed
4. Test with local dispatch
5. Update documentation

**Debugging**:
```bash
python3 agent.py --log-level DEBUG dev
```

## Best Practices

**Code Organization**:
- Keep `agent.py` focused on agent logic
- Extract complex utilities to separate files
- Use type hints for all function parameters
- Document all public functions with docstrings

**Configuration Management**:
- Use environment variables for all secrets
- Validate required variables on startup
- Provide clear error messages for missing config
- Use `.env.example` as documentation

**Error Handling**:
- Wrap API calls in try/except blocks
- Log errors with context
- Provide graceful degradation
- Don't expose sensitive info in error messages

**Testing**:
- Test with real phone numbers in development
- Validate SIP trunk configuration
- Check health before deployment
- Monitor logs for issues

**Documentation**:
- Update README.md when adding features
- Document environment variables
- Provide examples for common tasks
- Keep steering docs in sync with code
