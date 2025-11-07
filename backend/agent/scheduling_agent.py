"""
scheduling_agent.py
-------------------
Manual AI scheduling agent using a single super prompt.
This agent:
- Uses LLM to interpret user input and decide next action
- Handles JSON-based structured responses
- Fills placeholders (<AVAILABLE_SLOTS>, <CONFIRMATION_CODE>, etc.)
- Calls backend tools (mock APIs or RAG)
"""

import os
import json
from openai import OpenAI
from typing import List, Dict, Any
from dotenv import load_dotenv

from utils.placeholder_utils import fill_placeholders
from .prompts import PROMPT
from utils.chat_store import add_message, get_recent_messages

from api.calendly_integration import (
    get_availability_endpoint,
    book_appointment_endpoint,
    reschedule_appointment_endpoint,
    cancel_appointment_endpoint
)

from rag.faq_rag import retrieve_answer

load_dotenv()

def build_conversation_context(session_id: str) -> str:
    """
    Build conversation text from last 10 chat messages.
    """
    history = get_recent_messages(session_id, n=10)
    return "\n".join([f"{m['role'].capitalize()}: {m['message']}" for m in history])


def parse_llm_json(response_text: str) -> Dict[str, Any]:
    """
    Safely parse JSON output from the LLM.
    If invalid, attempt to auto-fix common errors.
    """
    print("response_text:", response_text)
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start != -1 and end != -1:
            try:
                return json.loads(response_text[start:end])
            except Exception:
                pass
        return {"action": "error", "response": "Sorry, I couldn’t process that correctly."}


def execute_action(action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform backend actions based on the LLM's JSON output.
    Returns data dictionary for placeholder filling.
    """
    data = {}
    try:
        if action == "check_availability":
            data = get_availability_endpoint(parameters)

        elif action == "book_appointment":
            if "patient" not in parameters:
                patient_fields = {k: parameters.get(k) for k in ["patient_name", "email", "phone"] if parameters.get(k)}
                parameters["patient"] = {
                    "name": patient_fields.get("patient_name", "Unknown"),
                    "email": patient_fields.get("email", ""),
                    "phone": patient_fields.get("phone", "")
                }
            data = book_appointment_endpoint(parameters)
            
        elif action == "reschedule_appointment":
            confirmation_code = parameters.get("confirmation_code")
            new_date = parameters.get("new_date")
            new_start_time = parameters.get("new_start_time")

            if not confirmation_code or not new_date or not new_start_time:
                data = {"error": "Missing required fields for rescheduling."}
            else:
                data = reschedule_appointment_endpoint(parameters)

        elif action == "cancel_appointment":
            confirmation_code = parameters.get("confirmation_code")
            if not confirmation_code:
                data = {"error": "Confirmation code is required to cancel an appointment."}
            else:
                data = cancel_appointment_endpoint(parameters)

        elif action == "answer_faq":
            topic = parameters.get("topic") or parameters.get("question") or ""
            if not topic.strip():
                data = {"faq_answer": "Could you please specify your question?"}
            else:
                try:
                    answer = retrieve_answer(topic)
                    data = {"faq_answer": answer}
                except Exception as e:
                    data = {"faq_answer": f"Sorry, I couldn’t fetch that info: {str(e)}"}

        else:
            data = {}

    except Exception as e:
        data = {"error": str(e)}

    return data

def run_agent(session_id: str) -> Dict[str, Any]:
    """
    Main agent pipeline:
    1. Build context from last 10 messages
    2. Send to LLM with Super Prompt
    3. Parse JSON response
    4. Execute action
    5. Replace placeholders
    6. Return final text
    """

    context_text = build_conversation_context(session_id)

    combined_input = f"{PROMPT}\n\nCHAT_HISTORY:\n{context_text}"

    llm_output = call_llm(combined_input)

    parsed = parse_llm_json(llm_output)

    action = parsed.get("action", "")
    parameters = parsed.get("parameters", {})
    base_response = parsed.get("response", "I'm not sure how to proceed.")

    data = execute_action(action, parameters)

    final_message = fill_placeholders(base_response, data)

    add_message(session_id, "agent", final_message)

    return {"message": final_message, "session_id": session_id}


def call_llm(prompt: str) -> str:

    OPENROUTER_API_BASE = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
    model = os.getenv("OPENROUTER_MODEL")
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))

    client = OpenAI(
        base_url=OPENROUTER_API_BASE,
        api_key=os.getenv("OPENROUTER_API_KEY", "api-key")
    )

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM error: {str(e)}"
