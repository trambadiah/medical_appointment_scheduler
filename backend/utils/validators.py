import re
from datetime import datetime, date
from typing import Optional

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format."""
    pattern = re.compile(r"^\+?[1-9]\d{1,14}$")
    return bool(pattern.match(phone))

def validate_appointment_time(start_time: datetime, end_time: datetime) -> bool:
    """Ensure end time is after start time and within working hours."""
    if start_time >= end_time:
        return False
    
    # Check if within 8 AM to 6 PM
    if start_time.hour < 8 or end_time.hour > 18:
        return False
        
    return True

def validate_future_date(dt: datetime) -> bool:
    """Check if the provided datetime is in the future."""
    return dt > datetime.now()

def validate_age(dob: date) -> int:
    """Calculate and validate age from date of birth."""
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age < 0 or age > 150:
        raise ValueError("Invalid date of birth provided.")
    return age
