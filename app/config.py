from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from typing import List

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "WhatsApp Microservice"
    
    # WhatsApp API Configuration
    WHATSAPP_API_TOKEN: str = os.getenv("WHATSAPP_API_TOKEN", "")
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    
    # Security
    API_KEY_NAME: str = "X-API-Key"
    API_KEY: str = os.getenv("API_KEY", "")
    
    # Security Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ALLOWED_HOSTS: List[str] = ["*"]  # In production, replace with actual hosts
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "100"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    ENFORCE_HTTPS: bool = os.getenv("ENFORCE_HTTPS", "True").lower() == "true"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]  # In production, replace with actual origins
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Application Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        case_sensitive = True

# Create global settings object
settings = Settings()
