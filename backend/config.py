import os
from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Apex Executive AI Enterprise"
    VERSION: str = "5.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    PORT: int = int(os.getenv("PORT", "8000"))

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "gemini")

    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./apex_memory.db")

    CEO_SECRET_TOKEN: str = os.getenv("CEO_SECRET_TOKEN", "apex_ceo_master_key_2026")
    CORS_ORIGINS: List[str] = ["*"]

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()
