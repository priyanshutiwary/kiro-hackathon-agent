# Proposed Agent Tools

10 tools to enhance the payment reminder voice agent's capabilities during customer calls.

---

## 🔥 High Priority (Implement First)

### 1. Payment Status Lookup
**What**: Check if invoice is paid in real-time from Zoho  
**When**: Customer says "I already paid this"  
**Why**: Avoid annoying customers who already paid  
**API**: `GET /api/invoices/status?invoice_number={number}`

```python
@llm.function_tool
async def check_payment_status(invoice_number: str) -> dict:
    """Check if invoice is paid. Returns: is_paid, amount_paid, balance_due"""
```

### 2. Payment Link Generator
**What**: Send payment link via SMS during call  
**When**: Customer wants to pay now but doesn't have invoice  
**Why**: Immediate payment = higher conversion  
**API**: `POST /api/invoices/send-payment-link`

```python
@llm.function_tool
async def send_payment_link(phone_number: str, invoice_id: str) -> str:
    """Generate and SMS payment link to customer"""
```

### 3. Invoice Details Lookup
**What**: Get invoice line items and details  
**When**: Customer asks "What is this charge for?"  
**Why**: Answer questions without human intervention  
**API**: `GET /api/invoices/details?invoice_number={number}`

```python
@llm.function_tool
async def get_invoice_details(invoice_number: str) -> dict:
    """Get invoice items, amounts, dates"""
```

---

## 📊 Medium Priority

### 4. Dispute Recording
**What**: Log customer disputes with details  
**When**: Customer says "This is wrong" or disputes charge  
**Why**: Capture details for follow-up  
**API**: `POST /api/invoices/dispute`

```python
@llm.function_tool
async def record_dispute(invoice_number: str, dispute_reason: str, details: str) -> bool:
    """Record dispute: incorrect_amount, service_issue, duplicate, other"""
```

### 5. Schedule Callback
**What**: Let customer choose callback time  
**When**: Customer says "Call me tomorrow at 3pm"  
**Why**: Respect preferences = higher answer rate  
**API**: `POST /api/reminders/schedule-callback`

```python
@llm.function_tool
async def schedule_callback(preferred_date: str, preferred_time: str, timezone: str) -> bool:
    """Schedule call at customer's preferred time"""
```

### 6. SMS Follow-up
**What**: Send SMS during/after call  
**When**: Customer prefers text or needs written confirmation  
**Why**: Multi-channel = better results  
**API**: `POST /api/sms/send`

```python
@llm.function_tool
async def send_sms_followup(phone_number: str, message_type: str) -> bool:
    """Send SMS: payment_reminder, payment_link, confirmation"""
```

---

## 💡 Lower Priority (Nice to Have)

### 7. Payment Plan Proposal
**What**: Offer installment plans  
**When**: Customer can't pay full amount  
**Why**: Collect partial payment vs nothing  
**API**: `POST /api/invoices/payment-plan`

```python
@llm.function_tool
async def propose_payment_plan(invoice_id: str, num_installments: int) -> dict:
    """Create 2-6 month payment plan"""
```

### 8. Transfer to Human
**What**: Escalate to human agent  
**When**: Issue too complex or customer requests  
**Why**: Handle edge cases gracefully  
**API**: `POST /api/calls/transfer`

```python
@llm.function_tool
async def transfer_to_human(reason: str, urgency: str) -> bool:
    """Transfer call to human: low, normal, high urgency"""
```

### 9. Update Contact Info
**What**: Update phone/email in Zoho  
**When**: Customer provides new contact details  
**Why**: Keep data current  
**API**: `PATCH /api/customers/update-contact`

```python
@llm.function_tool
async def update_contact_info(customer_id: str, new_phone: str, new_email: str) -> bool:
    """Update customer contact in Zoho"""
```

### 10. Call Notes
**What**: Add free-form notes  
**When**: Important details not in structured fields  
**Why**: Context for follow-up  
**API**: `POST /api/reminders/add-note`

```python
@llm.function_tool
async def add_call_note(note: str, category: str) -> bool:
    """Add note: promise_to_pay, dispute, callback_request, general"""
```

---

## 🏗️ Implementation

**Agent Side** (Python):
- Add tools to `PaymentAssistant` class in `agent/src/agents/payment_assistant.py`
- Use `@llm.function_tool` decorator (like existing `end_call`)
- Make async HTTP calls to backend APIs
- Handle errors gracefully

**Backend Side** (Next.js):
- Create API routes in `call_agent_smes/app/api/`
- Authenticate with HMAC signature or API key
- Validate inputs, return JSON
- Log all tool usage

**Security**:
- HMAC auth for all tool APIs
- Rate limit SMS/payment links
- Sanitize inputs
- Audit log everything

---

## 🚀 Rollout

**Phase 1** (Week 1-2): Payment Status, Payment Link, Invoice Details  
**Phase 2** (Week 3-4): Dispute, Callback, SMS  
**Phase 3** (Week 5-6): Payment Plan, Contact Update, Notes  
**Phase 4** (Future): Transfer to Human, Analytics

---

## 📈 Success Metrics

- Payment Link: Conversion rate (sent → paid)
- Status Lookup: Reduction in unnecessary calls
- Dispute: Time to resolution
- Callback: Answer rate improvement
- Overall: Payment collection rate increase

---

**Status**: Proposal | **Updated**: Jan 24, 2026
