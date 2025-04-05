import os
from typing import Optional, Dict, Any, List
from pydantic_settings import BaseSettings
from pydantic import validator, Field


class Settings(BaseSettings):
    """Application settings with validation.
    
    Loads values from environment variables and .env file.
    """
    
    # App info
    APP_NAME: str = "AGN-DB API"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Astrophysics AGN Database API"
    
    # Environment
    ENV: str = Field("development", env="ENVIRONMENT")
    DEBUG: bool = Field(True, env="DEBUG")
    
    # API configuration
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    ALLOWED_HOSTS: List[str] = Field(["*"], env="ALLOWED_HOSTS")
    
    # Database settings
    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PORT: int = Field(3306, env="DB_PORT")
    DB_USER: str = Field("root", env="DB_USER")
    DB_PASSWORD: str = Field("password", env="DB_PASSWORD")
    DB_NAME: str = Field("agndb", env="DB_NAME")
    DB_ECHO_LOG: bool = Field(False, env="DB_ECHO_LOG")
    DB_POOL_SIZE: int = Field(5, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(10, env="DB_MAX_OVERFLOW")
    DATABASE_URL: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field("simple", env="LOG_FORMAT")
    LOG_FILE_PATH: str = Field("logs/backend.log", env="LOG_FILE_PATH")
    LOG_ROTATION: str = Field("5 MB", env="LOG_ROTATION")
    LOG_RETENTION: str = Field("1 month", env="LOG_RETENTION")
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Build database URL from components if not provided directly."""
        if v:
            return v
            
        user = values.get("DB_USER")
        password = values.get("DB_PASSWORD")
        host = values.get("DB_HOST")
        port = values.get("DB_PORT")
        db = values.get("DB_NAME")
        
        # Use asyncmy as the driver for async SQLAlchemy with MariaDB
        return f"mariadb+asyncmy://{user}:{password}@{host}:{port}/{db}"
    
    class Config:
        """Pydantic config class."""
        
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings object
settings = Settings() 