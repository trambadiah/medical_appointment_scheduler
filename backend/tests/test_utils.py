import pytest
from datetime import datetime, timedelta, date
from backend.utils.validators import (
    validate_phone_number,
    validate_appointment_time,
    validate_future_date,
    validate_age
)

def test_validate_phone_number():
    assert validate_phone_number("+1234567890") == True
    assert validate_phone_number("12345") == True
    assert validate_phone_number("invalid") == False

def test_validate_appointment_time():
    today = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    later = today + timedelta(hours=1)
    assert validate_appointment_time(today, later) == True
    
    # Invalid: start after end
    assert validate_appointment_time(later, today) == False
    
    # Invalid: outside working hours (7 AM)
    early = today.replace(hour=7)
    assert validate_appointment_time(early, today) == False

def test_validate_future_date():
    future = datetime.now() + timedelta(days=1)
    past = datetime.now() - timedelta(days=1)
    assert validate_future_date(future) == True
    assert validate_future_date(past) == False

def test_validate_age():
    today = date.today()
    dob_20_years_ago = today.replace(year=today.year - 20)
    assert validate_age(dob_20_years_ago) == 20
    
    with pytest.raises(ValueError):
        future_dob = today.replace(year=today.year + 1)
        validate_age(future_dob)
