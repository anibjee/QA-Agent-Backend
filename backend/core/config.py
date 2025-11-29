import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Autonomous QA Agent"
    API_V1_STR: str = "/api/v1"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    CHROMA_PERSIST_DIRECTORY: str = "data/chroma_db"
    UPLOAD_DIRECTORY: str = "data/uploads"

    class Config:
        case_sensitive = True

settings = Settings()
