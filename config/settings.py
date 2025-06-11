from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "FastAPI MongoDB Backend"
    db_type: str = os.environ.get("DB_TYPE", "mongodb")
    db_name: str = os.environ.get("DB_NAME", "fastapi_db")
    db_url: str = os.environ.get("DB_URL", "mongodb://localhost:27017")
    cors_origins: list[str] = os.environ.get(
        "CORS_ORIGINS", "http://localhost:8000"
    ).split(",")
