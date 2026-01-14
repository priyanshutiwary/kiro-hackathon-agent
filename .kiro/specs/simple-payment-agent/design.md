# Design Document: Simple Payment Agent

## Overview

A straightforward payment reminder agent that receives context from the backend and conducts natural payment conversations without complex tools or response classification.

## Architecture

```
Backend → LiveKit → Simple Agent → Customer
```

## Components

### Context Handler
- Parse payment context from job metadata
- Extract customer and invoice information

### Conversation Engine  
- Generate payment-focused prompts
- Handle natural dialogue flow
- Maintain professional tone

## Data Models

### Payment Context
```python
customer_name: str
invoice_number: str  
amount_due: float
due_date: str
company_name: str
```

## Correctness Properties

### Property 1: Context Usage
*For any* valid payment context, the agent should use customer name and invoice details in conversation.

**Validates: Requirements 1.1-1.5, 2.1-2.3**

### Property 2: Professional Tone
*For any* payment conversation, the agent should maintain courteous and professional communication.

**Validates: Requirements 2.6**

## Testing Strategy

### Unit Tests
- Test context parsing
- Test conversation generation
- Test call management

### Integration Tests  
- Test end-to-end call flow
- Test with various payment contexts