import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Apex Executive AI Enterprise"
    VERSION: str = "4.9.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    
    # Free-Tier Inference: Google AI Studio (Gemini) or Groq
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "gemini")
    
    # Free-Tier Database: Supabase PostgreSQL + pgvector
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./apex_memory.db")
    
    # Security & CEO Authority
    CEO_SECRET_TOKEN: str = os.getenv("CEO_SECRET_TOKEN", "apex_ceo_master_key_2026")
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
