from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime

class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field(..., regex=r"^\+?[1-9]\d{1,14}$")
    date_of_birth: date

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PatientListResponse(BaseModel):
    patients: List[PatientResponse]
    total_count: int
    page: int
    size: int
