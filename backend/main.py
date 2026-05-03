from fastapi import FastAPI
from api.chat import router as chat_router
from api.patients import router as patients_router
from api.doctors import router as doctors_router
from rag.faq_rag import load_faq_data

app = FastAPI(title="Medical Appointment Scheduler API", version="1.0.0")

app.include_router(chat_router)
app.include_router(patients_router)
app.include_router(doctors_router)

@app.on_event("startup")
async def startup_event():
    """
    Load clinic FAQs into Chroma vector DB at app startup.
    """
    try:
        load_faq_data(force_reload=False)
        print("FAQ documents loaded into Chroma on startup.")
    except Exception as e:
        print(f"Failed to load FAQ data: {e}")