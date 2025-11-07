"""
booking_tool.py
----------------
Mock Calendly /book endpoint.

Books slots in memory
Prevents double-booking
Supports rescheduling and cancellation
Updates in-memory BOOKINGS shared across tools
"""

import json
import os
import random
import string
from typing import Dict, Any

SCHEDULE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "doctor_schedule.json")

BOOKINGS: Dict[str, Dict[str, Any]] = {}


def _load_schedule() -> Dict[str, Any]:
    """Load doctor schedule JSON file."""
    if not os.path.exists(SCHEDULE_PATH):
        return {}
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _generate_confirmation_code(length: int = 6) -> str:
    """Generate a random confirmation code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def book_appointment(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    POST /api/calendly/book (in-memory)
    Args:
        params: {
            "appointment_type": "consultation",
            "date": "2025-11-10",
            "start_time": "09:00",
            "patient": {...},
            "reason": "Headache"
        }
    """
    appointment_type = params.get("appointment_type", "consultation")
    date = params.get("date")
    start_time = params.get("start_time")
    patient = params.get("patient", {})
    reason = params.get("reason", "General consultation")

    # Load doctor schedule
    schedule = _load_schedule()
    if not (date and appointment_type and start_time):
        return {"status": "failed", "error": "Missing required fields."}

    if date not in schedule or appointment_type not in schedule[date]:
        return {"status": "failed", "error": "No schedule found for this date/type."}

    slots = schedule[date][appointment_type]
    slot = next((s for s in slots if s["start_time"] == start_time), None)
    if not slot or not slot.get("available", False):
        return {"status": "failed", "error": "Slot not available in schedule."}

    # Prevent double booking
    for b in BOOKINGS.values():
        details = b.get("details", {})
        if details.get("date") == date and details.get("start_time") == start_time:
            return {"status": "failed", "error": "That slot is already booked."}

    # Create booking record
    confirmation_code = _generate_confirmation_code()
    booking_id = f"APPT-{date.replace('-', '')}-{random.randint(100,999)}"

    booking = {
        "booking_id": booking_id,
        "status": "confirmed",
        "confirmation_code": confirmation_code,
        "details": {
            "appointment_type": appointment_type,
            "date": date,
            "start_time": start_time,
            "patient": patient,
            "reason": reason
        }
    }

    BOOKINGS[confirmation_code] = booking

    return booking


def reschedule_appointment(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    POST /api/calendly/reschedule (in-memory)
    Args:
        params: {
            "confirmation_code": "ABC123",
            "new_date": "2025-11-15",
            "new_start_time": "10:00"
        }
    """
    confirmation_code = params.get("confirmation_code")
    new_date = params.get("new_date")
    new_start_time = params.get("new_start_time")

    if not confirmation_code or not new_date or not new_start_time:
        return {"status": "failed", "error": "Missing required parameters."}

    if confirmation_code not in BOOKINGS:
        return {"status": "failed", "error": "Invalid confirmation code."}

    existing_booking = BOOKINGS[confirmation_code]
    old_date = existing_booking["details"]["date"]
    old_time = existing_booking["details"]["start_time"]

    # Prevent booking conflict
    for b in BOOKINGS.values():
        details = b.get("details", {})
        if details.get("date") == new_date and details.get("start_time") == new_start_time:
            return {"status": "failed", "error": "That slot is already booked."}

    # Load schedule and verify new slot availability
    schedule = _load_schedule()
    appointment_type = existing_booking["details"]["appointment_type"]
    if new_date not in schedule or appointment_type not in schedule[new_date]:
        return {"status": "failed", "error": "No schedule found for new date/type."}

    slots = schedule[new_date][appointment_type]
    slot = next((s for s in slots if s["start_time"] == new_start_time), None)
    if not slot or not slot.get("available", False):
        return {"status": "failed", "error": "New slot is not available."}

    # Update booking
    existing_booking["details"]["date"] = new_date
    existing_booking["details"]["start_time"] = new_start_time
    existing_booking["status"] = "rescheduled"

    BOOKINGS[confirmation_code] = existing_booking

    return {
        "status": "rescheduled",
        "confirmation_code": confirmation_code,
        "old_date": old_date,
        "old_time": old_time,
        "new_date": new_date,
        "new_start_time": new_start_time,
        "details": existing_booking["details"]
    }


def cancel_appointment(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    POST /api/calendly/cancel (in-memory)
    Args:
        params: {"confirmation_code": "ABC123"}
    """
    confirmation_code = params.get("confirmation_code")

    if not confirmation_code:
        return {"status": "failed", "error": "Confirmation code is required."}

    if confirmation_code not in BOOKINGS:
        return {"status": "failed", "error": "Invalid confirmation code or appointment not found."}

    canceled_booking = BOOKINGS.pop(confirmation_code)
    canceled_booking["status"] = "canceled"

    return {
        "status": "canceled",
        "confirmation_code": confirmation_code,
        "details": canceled_booking["details"]
    }


def get_all_bookings() -> Dict[str, Any]:
    """Return all active bookings (for debugging)."""
    return BOOKINGS
