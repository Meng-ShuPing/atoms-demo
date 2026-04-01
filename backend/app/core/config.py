from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    APP_NAME: str = "Atoms Demo"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./atoms_demo.db"

    # AI 配置
    AI_API_KEY: Optional[str] = None
    AI_MODEL: str = "qwen3.5-plus"

    # CORS 配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
