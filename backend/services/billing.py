from backend.models.billing import Billing
from backend.models.appointment import Appointment
from sqlalchemy.orm import Session
import uuid

class BillingService:
    def __init__(self, db: Session):
        self.db = db
        
    def generate_invoice(self, appointment_id: int, amount: float) -> Billing:
        app = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not app:
            raise ValueError("Appointment not found")
            
        bill = Billing(
            appointment_id=appointment_id,
            amount=amount,
            status="PENDING",
            transaction_id=str(uuid.uuid4())
        )
        self.db.add(bill)
        self.db.commit()
        self.db.refresh(bill)
        return bill
        
    def process_payment(self, billing_id: int, payment_method: str) -> bool:
        # Integration with Stripe or external payment gateway
        bill = self.db.query(Billing).filter(Billing.id == billing_id).first()
        if not bill:
            return False
            
        # Mocking payment processing
        bill.status = "PAID"
        bill.payment_method = payment_method
        self.db.commit()
        return True
