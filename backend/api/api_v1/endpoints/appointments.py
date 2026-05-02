from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api import deps
from backend.models.user import User
from backend.schemas.appointment import AppointmentCreate, AppointmentResponse
from backend.services.scheduling import SchedulingService

router = APIRouter()

@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    *,
    db: Session = Depends(deps.get_db),
    app_in: AppointmentCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    service = SchedulingService(db)
    try:
        app = service.schedule_appointment(
            patient_id=app_in.patient_id,
            doctor_id=app_in.doctor_id,
            scheduled_time=app_in.scheduled_time
        )
        return app
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
