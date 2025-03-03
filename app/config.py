from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

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

    class Config:
        case_sensitive = True

# Create global settings object
settings = Settings()
