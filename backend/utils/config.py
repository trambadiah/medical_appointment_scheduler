from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Medical Appointment Scheduler"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "super_secret_placeholder_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database Settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "medical_db"
    
    # OpenAI / AI Settings
    OPENAI_API_KEY: Optional[str] = None
    MODEL_NAME: str = "gpt-4-turbo"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
