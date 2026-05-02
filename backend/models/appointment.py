from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.db.base_class import Base

class Appointment(Base):
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    patient_id = Column(Integer, ForeignKey("patient.id"))
    scheduled_time = Column(DateTime, index=True)
    duration_minutes = Column(Integer, default=30)
    status = Column(String(50), default="SCHEDULED") # SCHEDULED, COMPLETED, CANCELLED
    notes = Column(Text)
    
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    billing = relationship("Billing", back_populates="appointment", uselist=False)
