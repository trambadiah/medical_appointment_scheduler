from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.appointment import Appointment
from backend.schemas.appointment import AppointmentCreate
from datetime import datetime

class CRUDAppointment:
    def get_patient_appointments(self, db: Session, patient_id: int) -> List[Appointment]:
        return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()

    def check_conflict(self, db: Session, doctor_id: int, time: datetime) -> bool:
        # Complex conflict checking logic here
        conflict = db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.scheduled_time == time,
            Appointment.status == "SCHEDULED"
        ).first()
        return conflict is not None

appointment = CRUDAppointment()
