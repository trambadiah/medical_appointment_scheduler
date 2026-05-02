from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.base_class import Base

class Patient(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    date_of_birth = Column(Date)
    blood_type = Column(String(5))
    emergency_contact = Column(String)
    insurance_provider = Column(String)
    insurance_policy_number = Column(String)
    
    user = relationship("User")
    appointments = relationship("Appointment", back_populates="patient")
