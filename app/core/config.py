from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application configuration settings
    """
    # Database
    database_url: str = "sqlite:///./taskpilot.db"
      # Security
    secret_key: str = "your-secret-key-here"  # fallback value
    jwt_secret_key: str = "your-jwt-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
      # AI Configuration
    ai_provider: str = "mock"  # openrouter, groq, huggingface, mock
    ai_api_key: Optional[str] = None
      # Legacy OpenAI Configuration (for backward compatibility)
    openai_api_key: Optional[str] = None
    
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    redis_db: int = 0
    redis_ttl: int = 3600  # Cache TTL in seconds (1 hour default)
    
    # App settings
    app_name: str = "TaskPilot"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API settings
    api_v1_prefix: str = "/api"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Single instance of settings
settings = Settings()
