# Implementation Plan: Simple Payment Agent

## Overview

Transform the appointment agent into a simple payment reminder agent that accepts context from backend and conducts natural payment conversations.

## Tasks

- [x] 1. Parse payment context from backend
  - Extract customer_name, invoice_number, amount_due, due_date, company_name from job metadata
  - Handle missing context gracefully with default messages
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 2. Replace appointment instructions with payment instructions
  - Remove Kyle appointment references
  - Create payment reminder prompt using context
  - Include invoice details and due date in instructions
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 3. Update greeting and conversation flow
  - Greet customer by name from context
  - Mention specific invoice number and amount
  - Explain payment due date clearly
  - Ask if customer has questions about the invoice
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 4. Simplify call management
  - Keep existing end_call function
  - Set reasonable call timeout (keep current 600 seconds)
  - Handle customer requests to end call
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 5. Update agent instructions for professional tone
  - Ensure polite and respectful language
  - Handle various customer responses naturally
  - Maintain professional demeanor throughout
  - _Requirements: 2.5, 2.6_

- [ ]* 6. Test with sample contexts
  - Test with different payment scenarios
  - Verify professional conversation flow
  - Ensure context is used correctly

## Notes

- Keep it simple - no complex tools or response classification yet
- Focus on natural conversation using payment context
- Maintain existing LiveKit integration
- Professional tone is key for payment conversations