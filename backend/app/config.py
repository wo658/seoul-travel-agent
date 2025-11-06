"""Application configuration settings."""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # App
    APP_NAME: str = "Seoul Travel Agent"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"  # development, docker, production

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8081"]

    # Database
    # Local development: SQLite (fast, no Docker needed)
    # Docker/Production: PostgreSQL
    DATABASE_URL: str = "sqlite:///./seoul_travel.db"

    # AI/LLM
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Seoul Open API
    SEOUL_OPENAPI_KEY: str = ""

    # Auth
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
