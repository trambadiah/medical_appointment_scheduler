from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.crud.crud_appointment import appointment as crud_appointment
from backend.models.appointment import Appointment

class SchedulingService:
    def __init__(self, db: Session):
        self.db = db

    def schedule_appointment(self, patient_id: int, doctor_id: int, scheduled_time: datetime) -> Appointment:
        if crud_appointment.check_conflict(self.db, doctor_id, scheduled_time):
            raise ValueError("Doctor is already booked at this time.")
        
        # Verify working hours
        if scheduled_time.hour < 8 or scheduled_time.hour >= 18:
            raise ValueError("Appointments must be between 8 AM and 6 PM.")
            
        new_app = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            scheduled_time=scheduled_time,
            status="SCHEDULED"
        )
        self.db.add(new_app)
        self.db.commit()
        self.db.refresh(new_app)
        return new_app
