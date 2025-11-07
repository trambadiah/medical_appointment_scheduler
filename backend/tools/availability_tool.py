"""
availability_tool.py
--------------------
Mock implementation of the Calendly /availability endpoint.

Reads schedule from doctor_schedule.json
Checks in-memory bookings to exclude already booked slots
Prevents suggesting double-booked times
"""

import json
import os
from typing import Dict, Any, List
from .booking_tool import BOOKINGS


# Path to schedule file
SCHEDULE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "doctor_schedule.json")


def _load_schedule() -> Dict[str, Any]:
    """Load doctor schedule JSON file."""
    if not os.path.exists(SCHEDULE_PATH):
        return {}
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_booked_slots(date: str) -> List[str]:
    """Get a list of booked start times for the given date from in-memory bookings."""
    booked = []
    for booking in BOOKINGS.values():
        details = booking.get("details", {})
        if details.get("date") == date:
            booked.append(details.get("start_time"))
    return booked


def get_availability(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    GET /api/calendly/availability (mocked, in-memory)
    Args:
        params: {
            "date": "2025-11-10",
            "appointment_type": "consultation"
        }
    Returns:
        {
            "date": "2025-11-10",
            "appointment_type": "consultation",
            "available_slots": [
                {"date": "2025-11-10", "start_time": "09:00", "end_time": "09:30"}
            ]
        }
    """
    date = params.get("date")
    appointment_type = params.get("appointment_type", "consultation")

    schedule = _load_schedule()
    if not date or date not in schedule or appointment_type not in schedule[date]:
        return {"date": date, "appointment_type": appointment_type, "available_slots": []}

    slots = schedule[date][appointment_type]
    booked_times = _get_booked_slots(date)

    available = []
    for s in slots:
        if s.get("available", False) and s["start_time"] not in booked_times:
            available.append({
                "date": date,
                "start_time": s["start_time"],
                "end_time": s["end_time"]
            })

    return {
        "date": date,
        "appointment_type": appointment_type,
        "available_slots": available
    }
