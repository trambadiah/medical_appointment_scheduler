from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.base_class import Base

class Doctor(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    specialty = Column(String, index=True)
    license_number = Column(String, unique=True, index=True)
    years_experience = Column(Integer)
    is_accepting_patients = Column(Boolean, default=True)
    
    user = relationship("User")
    appointments = relationship("Appointment", back_populates="doctor")
