# Requirements Document

## Introduction

This document specifies the requirements for a simple payment reminder voice agent that receives context from the backend and conducts basic payment conversations with customers.

## Glossary

- **Agent**: The voice agent that makes payment reminder calls
- **Backend**: The main system that provides payment context
- **Customer**: The person receiving the payment call
- **Context**: Payment information passed from backend

## Requirements

### Requirement 1: Context Reception

**User Story:** As an agent, I want to receive payment context from the backend, so that I can make informed payment calls.

#### Acceptance Criteria

1. THE Agent SHALL receive customer name from backend context
2. THE Agent SHALL receive invoice number from backend context  
3. THE Agent SHALL receive amount due from backend context
4. THE Agent SHALL receive due date from backend context
5. THE Agent SHALL receive company name from backend context

### Requirement 2: Basic Payment Conversations

**User Story:** As an agent, I want to have natural payment conversations, so that customers understand their payment obligations.

#### Acceptance Criteria

1. THE Agent SHALL greet customers by name
2. THE Agent SHALL mention the invoice number and amount due
3. THE Agent SHALL explain when payment is due
4. THE Agent SHALL ask if customer has any questions
5. THE Agent SHALL listen to customer responses naturally
6. THE Agent SHALL maintain professional tone throughout

### Requirement 3: Simple Call Management

**User Story:** As an agent, I want to manage calls properly, so that conversations are effective and polite.

#### Acceptance Criteria

1. THE Agent SHALL end calls when customers request it
2. THE Agent SHALL end calls after reasonable conversation time
3. THE Agent SHALL handle customer hang-ups gracefully