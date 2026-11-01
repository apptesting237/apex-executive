import os
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    PROJECT_NAME: str = "Apex Executive AI Enterprise"
    VERSION: str = "5.1.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'apex_memory.db'}",
    )
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", str(BASE_DIR / "apex_memory.db"))

    # LLMs / providers
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq").lower()

    # GitHub / OmniRoute hooks
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_REPO: str = os.getenv("GITHUB_REPO", "apptesting237/apex-executive")
    OMNIR_ROUTE_URL: str = os.getenv("OMNIR_ROUTE_URL", "")
    OMNIR_ROUTE_TOKEN: str = os.getenv("OMNIR_ROUTE_TOKEN", "")

    # Security / CEO auth
    CEO_SECRET_TOKEN: str = os.getenv("CEO_SECRET_TOKEN", "apex_ceo_master_key_2026")
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
