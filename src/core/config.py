from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "chat-api"
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@db:5432/postgres",
    )
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
