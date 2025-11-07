"""
calendly_integration.py
-----------------------
Mock Calendly API integration layer for the scheduling agent.

Provides in-memory endpoints for:
- GET /api/calendly/availability
- POST /api/calendly/book
- POST /api/calendly/reschedule
- POST /api/calendly/cancel

Integrates with:
- availability_tool.py
- booking_tool.py

Maintains in-memory BOOKINGS state.
"""

from typing import Dict, Any
from tools.availability_tool import get_availability
from tools.booking_tool import (
    book_appointment,
    reschedule_appointment,
    cancel_appointment,
    BOOKINGS,
)


def get_availability_endpoint(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates GET /api/calendly/availability
    """
    return get_availability(query_params)


def book_appointment_endpoint(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates POST /api/calendly/book
    """
    return book_appointment(body)


def reschedule_appointment_endpoint(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates POST /api/calendly/reschedule
    """
    return reschedule_appointment(body)


def cancel_appointment_endpoint(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates POST /api/calendly/cancel
    """
    return cancel_appointment(body)


def get_all_bookings() -> Dict[str, Any]:
    """Return current in-memory bookings."""
    return BOOKINGS
