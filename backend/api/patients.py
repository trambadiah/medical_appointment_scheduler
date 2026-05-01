from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.patient import PatientCreate, PatientResponse, PatientListResponse
from datetime import datetime

router = APIRouter(prefix="/patients", tags=["patients"])

# Mock DB
patients_db = []

@router.post("/", response_model=PatientResponse, status_code=201)
async def create_patient(patient: PatientCreate):
    new_patient = PatientResponse(
        id=len(patients_db) + 1,
        **patient.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    patients_db.append(new_patient)
    return new_patient

@router.get("/", response_model=List[PatientResponse])
async def get_patients(skip: int = 0, limit: int = 10):
    return patients_db[skip : skip + limit]

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: int):
    for p in patients_db:
        if p.id == patient_id:
            return p
    raise HTTPException(status_code=404, detail="Patient not found")
