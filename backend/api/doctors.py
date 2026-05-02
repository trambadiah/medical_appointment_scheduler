from fastapi import APIRouter, HTTPException
from typing import List
from ..models.doctor import DoctorCreate, DoctorResponse
from datetime import datetime

router = APIRouter(prefix="/doctors", tags=["doctors"])

# Mock DB
doctors_db = []

@router.post("/", response_model=DoctorResponse, status_code=201)
async def create_doctor(doctor: DoctorCreate):
    new_doctor = DoctorResponse(
        id=len(doctors_db) + 1,
        **doctor.dict(),
        is_active=True,
        created_at=datetime.now()
    )
    doctors_db.append(new_doctor)
    return new_doctor

@router.get("/", response_model=List[DoctorResponse])
async def get_doctors():
    return doctors_db

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(doctor_id: int):
    for d in doctors_db:
        if d.id == doctor_id:
            return d
    raise HTTPException(status_code=404, detail="Doctor not found")
