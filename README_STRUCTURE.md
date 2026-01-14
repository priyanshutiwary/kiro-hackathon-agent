# Project Structure Documentation

This document explains the modular architecture of the Payment Reminder Voice Agent and how the code is organized for maintainability and scalability.

## Directory Structure

```
agent/
├── main.py                          # Main application entry point
├── agent.py                         # Legacy compatibility wrapper
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .env.local                       # Local environment configuration (not in git)
├── livekit.toml                     # LiveKit configuration
├── outbound-trunk-example.json      # SIP trunk configuration template
├── README.md                        # Main documentation
├── README_STRUCTURE.md              # This file - architecture documentation
└── src/                             # Source code package
    ├── __init__.py                  # Package initialization
    ├── agents/                      # Agent implementations
    │   ├── __init__.py
    │   └── payment_assistant.py     # Core payment reminder agent
    ├── models/                      # Data models and structures
    │   ├── __init__.py
    │   └── payment_context.py       # Payment context data model
    ├── services/                    # Business logic services
    │   ├── __init__.py
    │   ├── call_service.py          # Call management and SIP operations
    │   └── greeting_service.py      # Professional greeting generation
    ├── utils/                       # Utility functions
    │   ├── __init__.py
    │   └── context_parser.py        # Metadata parsing utilities
    └── config/                      # Configuration management
        ├── __init__.py
        └── settings.py              # Application settings and validation
```

## Module Responsibilities

### Core Application (`main.py`)
- **Purpose**: Main entry point that orchestrates the entire application
- **Responsibilities**:
  - Initialize LiveKit connection
  - Parse payment context from job metadata
  - Set up outbound SIP calls
  - Create and configure the payment assistant agent
  - Manage agent session lifecycle
  - Handle call timeout and cleanup

### Legacy Compatibility (`agent.py`)
- **Purpose**: Maintains backward compatibility with existing deployments
- **Responsibilities**:
  - Import and delegate to the new modular structure
  - Ensure existing scripts and deployment processes continue to work
  - Provide migration path for users upgrading from the monolithic version

### Agents Package (`src/agents/`)

#### PaymentAssistant (`payment_assistant.py`)
- **Purpose**: Core agent implementation with professional communication capabilities
- **Responsibilities**:
  - Build comprehensive professional instructions for the LLM
  - Handle customer interactions with empathy and professionalism
  - Provide specific response templates for various customer scenarios
  - Manage call termination through the `end_call` tool
  - Maintain professional demeanor throughout conversations

**Key Features**:
- Professional communication standards with courteous language
- Intelligent handling of various customer responses (already paid, needs time, disputes, etc.)
- Empathetic and solution-focused conversation management
- Graceful call termination with polite closing messages

### Models Package (`src/models/`)

#### PaymentContext (`payment_context.py`)
- **Purpose**: Data structure for payment-related information
- **Responsibilities**:
  - Store customer and invoice details
  - Provide default values for missing information
  - Ensure type safety and data validation
  - Support string representation for debugging

**Data Fields**:
- `customer_name`: Customer's name (default: "valued customer")
- `invoice_number`: Invoice identifier (default: "your invoice")
- `amount_due`: Outstanding amount (optional, formatted as currency)
- `due_date`: Payment due date (default: "as soon as possible")
- `company_name`: Calling company name (default: "our company")

### Services Package (`src/services/`)

#### CallService (`call_service.py`)
- **Purpose**: Manage SIP call operations and lifecycle
- **Responsibilities**:
  - Set up outbound SIP calls through LiveKit
  - Extract phone numbers from various metadata formats
  - Handle JSON and plain text metadata parsing
  - Manage participant identity and room operations
  - Provide logging for call setup operations

#### GreetingService (`greeting_service.py`)
- **Purpose**: Generate professional and contextual greeting messages
- **Responsibilities**:
  - Create structured, professional greeting flows
  - Incorporate payment context into personalized messages
  - Ensure courteous and respectful language
  - Provide clear conversation structure (greeting → details → due date → questions)
  - Generate instructions for natural conversation delivery

**Greeting Structure**:
1. Professional greeting with customer name
2. Polite invoice details presentation
3. Clear due date explanation
4. Helpful question prompts for customer engagement

### Utils Package (`src/utils/`)

#### ContextParser (`context_parser.py`)
- **Purpose**: Parse and validate payment context from job metadata
- **Responsibilities**:
  - Handle both JSON and plain text metadata formats
  - Gracefully handle parsing errors and missing data
  - Provide fallback values for incomplete context
  - Log parsing issues for debugging
  - Support legacy phone number format

**Parsing Logic**:
- Detects JSON format by checking for opening brace
- Extracts structured payment data from JSON
- Falls back to treating metadata as phone number for legacy compatibility
- Provides comprehensive error handling and logging

### Config Package (`src/config/`)

#### Settings (`settings.py`)
- **Purpose**: Centralized configuration management and validation
- **Responsibilities**:
  - Load environment variables with proper defaults
  - Validate required configuration on startup
  - Provide type-safe access to configuration values
  - Define application constants and timeouts
  - Support different environments (development, production)

**Configuration Areas**:
- Call timeout settings (600 seconds default)
- SIP trunk configuration
- Agent naming and identification
- STT/TTS model specifications
- Environment variable validation

## Design Principles

### Separation of Concerns
Each module has a single, well-defined responsibility:
- **Agents**: Handle conversation logic and customer interaction
- **Models**: Define data structures and validation
- **Services**: Implement business logic and external integrations
- **Utils**: Provide reusable utility functions
- **Config**: Manage application configuration

### Type Safety
- All functions include proper type hints
- Optional parameters are clearly marked
- Return types are explicitly defined
- Data models use type annotations for all fields

### Error Handling
- Graceful degradation when data is missing or invalid
- Comprehensive logging for debugging and monitoring
- Fallback values for optional configuration
- Clear error messages for configuration issues

### Extensibility
- New services can be easily added to the `services/` package
- Additional data models can be created in `models/`
- New utility functions belong in `utils/`
- Agent behavior can be extended through the `agents/` package

### Maintainability
- Clear module boundaries prevent tight coupling
- Each file has a focused purpose and limited scope
- Dependencies are explicit and minimal
- Code is self-documenting with clear naming

## Migration from Monolithic Structure

### Backward Compatibility
The `agent.py` file serves as a compatibility layer:
- Existing deployment scripts continue to work
- Same command-line interface is maintained
- Environment variables remain unchanged
- No breaking changes for current users

### Gradual Migration
Users can migrate at their own pace:
1. **Immediate**: Use `python3 main.py` instead of `python3 agent.py`
2. **Development**: Modify individual modules in `src/` for customization
3. **Advanced**: Extend the architecture with new services and models

### Benefits of New Structure
- **Easier Testing**: Individual modules can be tested in isolation
- **Better Debugging**: Issues can be traced to specific modules
- **Simpler Maintenance**: Changes are localized to relevant modules
- **Enhanced Collaboration**: Multiple developers can work on different modules
- **Future Growth**: New features can be added without affecting existing code

## Development Workflow

### Adding New Features
1. **Identify the appropriate package** (agents, models, services, utils, config)
2. **Create new module** following existing naming conventions
3. **Add proper type hints** and documentation
4. **Include error handling** and logging
5. **Update imports** in `main.py` if needed
6. **Test the module** in isolation

### Modifying Existing Features
1. **Locate the relevant module** based on functionality
2. **Make focused changes** within the module's responsibility
3. **Maintain backward compatibility** when possible
4. **Update documentation** if interfaces change
5. **Test integration** with other modules

### Best Practices
- Keep modules focused on their single responsibility
- Use dependency injection rather than global state
- Add comprehensive logging for debugging
- Include type hints for all function parameters and returns
- Write self-documenting code with clear variable names
- Handle errors gracefully with appropriate fallbacks