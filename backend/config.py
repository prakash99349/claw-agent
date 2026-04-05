from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: Optional[str] = ""
    OPENAI_API_KEY: Optional[str] = ""
    NVIDIA_API_KEY: Optional[str] = ""
    GEMINI_API_KEY: Optional[str] = ""
    GITHUB_PAT: Optional[str] = ""
    GITHUB_REPO: str = "ultraworkers/claw-code"
    GITHUB_DEFAULT_BRANCH: str = "main"
    DEFAULT_MODEL: str = "claude-sonnet-4-6"
    MAX_CONTEXT_TOKENS: int = 100_000
    DATABASE_URL: str = "sqlite+aiosqlite:///./sessions.db"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
