# Medical Appointment Scheduling Agent - Technical Overview

This document provides a **brief summary** of the system setup, design, scheduling logic, and testing approach for the Medical Appointment Scheduling Agent.

---

## Setup Instructions

### Calendly API Setup (Optional)
- Default: Uses mock Calendly APIs (`/api/calendly/availability` and `/api/calendly/book`).
- To use the real API:
  1. Create an app at [Calendly Developer Portal](https://developer.calendly.com).
  2. Add your API key to `.env`:
     ```bash
     CALENDLY_API_KEY=your_real_api_key
     CALENDLY_ORG_URL=https://api.calendly.com
     ```
  3. Update `api/calendly_integration.py` to point to real endpoints.

### Environment Variables
Create a `.env` file in your root directory:
```bash
OPENROUTER_API_BASE=
OPENROUTER_API_KEY=
OPENROUTER_MODEL=
LLM_TEMPERATURE=
EMBEDDING_MODEL=
```

### Running the Application
```bash

uvicorn main:app --reload
```

---

## System Design

### Chat Flow
```
First message will create session and generate session id to store chat in memory.
Further messages will have session id in request body to preserve continutiy of the chat.
```
### Agent Conversation Flow
```
User → LLM (Super Prompt) → JSON (action + params + response)
     → execute_action(action)
     → Backend Tool (Calendly / RAG)
     → Placeholder replacement
     → Final agent reply
```

- The agent maintains conversation context in memory.
- All logic is handled by `agent/scheduling_agent.py`.

### Calendly Integration Approach
| Mode | Description |
|------|--------------|
| **Mock Mode** | Uses in-memory schedule and bookings (default) |
| **Real API Mode** | Integrates with Calendly REST API using API key |

### RAG Pipeline for FAQs
| Step | Component | Function |
|------|------------|-----------|
| 1 | `clinic_info.json` | FAQ data source |
| 2 | `embeddings.py` | Generates embeddings via Ollama |
| 3 | `vector_store.py` | Stores embeddings in Chroma |
| 4 | `faq_rag.py` | Retrieves answers for semantic FAQ queries |

### Tool Calling Strategy
LLM outputs structured JSON:
```json
{
  "action": "book_appointment",
  "parameters": {"date": "2025-11-10", "appointment_type": "consultation"},
  "response": "Appointment booked for <DATE> at <TIME>."
}
```
→ The agent executes corresponding backend logic and fills placeholders dynamically.

---

## Scheduling Logic

### How Available Slots Are Determined
- Loads doctor schedule from `data/doctor_schedule.json`.
- Filters by date, appointment type, and availability.
- Removes already booked slots from in-memory booking store.

### Appointment Type Handling
| Type | Duration | Description |
|------|-----------|-------------|
| consultation | 30 mins | Default visit |
| followup | 20 mins | Returning patients |
| physical | 45 mins | Checkups |
| specialist | 60 mins | Advanced cases |

### Conflict Prevention
- Double booking is prevented by checking booked slots in memory.
- Booking requests for unavailable times are gracefully rejected.

---

## Testing

### Example Conversations

**User:** I need to see a doctor  

**Agent:** Sure! What’s the reason for your visit today?  

**User:** I’ve been having headaches for the past few days.  

**Agent:** I understand. For recurring headaches, I recommend a general consultation (30 minutes). Does that sound good, or would you prefer a longer specialist consultation?.  

**User:** General consultation is fine.  

**Agent:** Perfect! When would you like to come in? Do you prefer a morning or afternoon appointment?

**User:** November 10 morning will work

**Agent:** Sure. Let me check our available afternoon slots for this week...
Here’s what I found:
- Nov 10 at 2:00 PM
- Nov 10 at 3:30 PM

Which one works best for you?

**User:** 3:30 PM sounds good.

**Agent:** Great! Before I confirm, I’ll need a few details:

- Your full name
- Email address 
- Phone number

**User:** Sure. My name is John Doe, email is john@example.com, phone number is 1234567890.

**Agent:** Thank you, John! Your 30-minute consultation is confirmed for Wednesday, November 12th at 3:30 PM. Confirmation Code: ABC123. You’ll receive an email with all details shortly.

**User:** Where exactly is your clinic located?

**Agent:** Our clinic is located at 123 Health Street, Wellness City, near Central Park, on the second floor of the Wellness Plaza Building.



### Edge Cases Covered
| Case | Behavior |
|------|-----------|
| Double booking | Prevented; user prompted to choose another slot |
| Invalid input | Model asks for clarification |
| Unknown FAQ | Graceful fallback message |
| Missing user info | Agent requests missing details |
| LLM invalid JSON | Auto-corrected by parser |

---

**In summary:**  
This system integrates conversational AI with backend scheduling and retrieval-augmented generation (RAG) to automate clinic operations — all running locally using **FastAPI + LangChain + Ollama + Chroma**.