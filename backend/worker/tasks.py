from backend.worker.celery_app import celery_app
import time
import logging

logger = logging.getLogger(__name__)

@celery_app.task(acks_late=True)
def send_appointment_reminder(email: str, time: str) -> str:
    # Simulate sending email
    logger.info(f"Sending email to {email} for appointment at {time}")
    time.sleep(2)
    return f"Reminder sent to {email}"

@celery_app.task
def generate_monthly_reports() -> str:
    # Heavy data processing
    logger.info("Generating monthly hospital utilization reports...")
    time.sleep(10)
    return "Report generation complete."
