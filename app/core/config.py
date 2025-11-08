import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    PROJECT_NAME: str = "Universal Tourist Guide API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # База данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tourist_guide.db")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "секретный-ключ-изменить-в-продакшене")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 дней
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()