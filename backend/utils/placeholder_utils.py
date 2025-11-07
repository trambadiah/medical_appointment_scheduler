"""
placeholder_utils.py
---------------------
Utility to replace LLM-generated placeholders in agent responses
with real data returned from backend APIs or RAG systems.

Supported placeholders:
- <AVAILABLE_SLOTS>
- <CONFIRMATION_CODE>
- <FAQ_ANSWER>
"""

from typing import Dict, Any, List


def _format_slots(slots: List[Dict[str, str]]) -> str:
    """
    Format available appointment slots as a readable list.
    """
    if not slots:
        return "No available slots. Would you like to try another date?"
    formatted = "\n".join(
        [f"- {slot.get('date', '?')} at {slot.get('start_time', '?')}" for slot in slots]
    )
    return formatted


def fill_placeholders(response_text: str, data: Dict[str, Any]) -> str:
    """
    Replace placeholders in the response_text with actual values
    from the provided backend data.

    Args:
        response_text (str): The LLM's response text containing placeholders.
        data (dict): Backend data containing dynamic values.

    Returns:
        str: The final text with placeholders replaced.
    """
    if not response_text:
        return ""

    # Replace <AVAILABLE_SLOTS>
    if "<AVAILABLE_SLOTS>" in response_text:
        slots = data.get("available_slots", [])
        response_text = response_text.replace("<AVAILABLE_SLOTS>", _format_slots(slots))

    # Replace <CONFIRMATION_CODE>
    if "<CONFIRMATION_CODE>" in response_text:
        response_text = response_text.replace(
            "<CONFIRMATION_CODE>",
            data.get("confirmation_code", "N/A")
        )

    # Replace <FAQ_ANSWER>
    if "<FAQ_ANSWER>" in response_text:
        response_text = response_text.replace(
            "<FAQ_ANSWER>",
            data.get("faq_answer", "I'm not sure, but you can check with the front desk.")
        )

    # Replace <CANCEL_CONFIRMATION>
    if "<CANCEL_CONFIRMATION>" in response_text:
        response_text = response_text.replace(
            "<CANCEL_CONFIRMATION>",
            data.get("cancel_message", "Your appointment has been successfully cancelled.")
        )

    # Replace <RESCHEDULE_CONFIRMATION>
    if "<RESCHEDULE_CONFIRMATION>" in response_text:
        response_text = response_text.replace(
            "<RESCHEDULE_CONFIRMATION>",
            data.get("reschedule_message", "Your appointment has been rescheduled.")
        )

    # Fallback: clean up stray placeholders (safety)
    known_placeholders = [
        "<AVAILABLE_SLOTS>",
        "<CONFIRMATION_CODE>",
        "<FAQ_ANSWER>",
        "<CANCEL_CONFIRMATION>",
        "<RESCHEDULE_CONFIRMATION>",
    ]
    for ph in known_placeholders:
        if ph in response_text:
            response_text = response_text.replace(ph, "[Data unavailable]")

    return response_text.strip()
