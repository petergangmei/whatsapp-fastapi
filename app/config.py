import os
from typing import List
from dotenv import load_dotenv
from app.logger import logger

# Load environment variables from .env file with override=True to ensure values are loaded
load_dotenv(override=True)

# Debug logging for raw environment variables
raw_api_key = os.getenv('API_KEY')
logger.debug("=== Raw Environment Variables Debug Info ===")
logger.debug(f"Raw API_KEY from environment: '{raw_api_key}'")
logger.debug(f"Raw API_KEY type: {type(raw_api_key)}")
logger.debug(f"Raw API_KEY length: {len(raw_api_key) if raw_api_key else 0}")

class Settings:
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "WhatsApp Microservice"
    
    # WhatsApp API Configuration
    WHATSAPP_API_TOKEN: str = os.getenv("WHATSAPP_API_TOKEN", "")
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("PHONE_NUMBER_ID", "")  # Reading from PHONE_NUMBER_ID env var
    
    # Security Settings
    API_KEY_NAME: str = "X-API-Key"  # Name of the header for API key
    API_KEY: str = os.getenv("API_KEY", "").strip()  # Strip whitespace from API key
    ENFORCE_HTTPS: bool = os.getenv("ENFORCE_HTTPS", "true").lower() == "true"
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "100"))
    RATE_LIMIT_WINDOW_SECONDS: int = 60  # Default window of 60 seconds
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "debug").upper()

    def __init__(self):
        # Validate API key on initialization
        if not self.API_KEY:
            logger.warning("API_KEY is empty or not set in environment")
        else:
            logger.debug(f"API_KEY initialized with length: {len(self.API_KEY)}")
        
        # Validate WhatsApp configuration
        if not self.WHATSAPP_API_TOKEN:
            logger.warning("WHATSAPP_API_TOKEN is not set")
        if not self.WHATSAPP_PHONE_NUMBER_ID:
            logger.warning("WHATSAPP_PHONE_NUMBER_ID is not set")

# Create settings instance
settings = Settings()

# Debug print to verify API key loading
logger.debug("=== Settings Instance Debug Info ===")
logger.debug(f"Final API Key from settings (first 4 chars): {settings.API_KEY[:4] if settings.API_KEY else 'None'}")
logger.debug(f"Final API Key length in settings: {len(settings.API_KEY)}")
logger.debug(f"Final API Key type in settings: {type(settings.API_KEY)}")
logger.debug(f"Expected header name: {settings.API_KEY_NAME}")
logger.debug(f"WhatsApp Phone Number ID: {settings.WHATSAPP_PHONE_NUMBER_ID}")
