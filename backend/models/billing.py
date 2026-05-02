from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.db.base_class import Base
from datetime import datetime

class Billing(Base):
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointment.id"))
    amount = Column(Float, nullable=False)
    status = Column(String, default="PENDING") # PENDING, PAID, REFUNDED
    payment_method = Column(String)
    transaction_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    appointment = relationship("Appointment", back_populates="billing")
