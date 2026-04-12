from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import time, datetime

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialty: str
    email: EmailStr
    bio: Optional[str] = None
    years_of_experience: int = Field(ge=0)

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class DoctorSchedule(BaseModel):
    doctor_id: int
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    is_available: bool = True
