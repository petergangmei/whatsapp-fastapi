from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config import settings
from app.logger import logger

api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify the API key from the request header.
    
    Args:
        api_key: The API key from the request header
        
    Returns:
        str: The verified API key
        
    Raises:
        HTTPException: If the API key is invalid or missing
    """
    # Enhanced debug logging
    logger.debug("=== API Key Verification Debug Info ===")
    logger.debug(f"Header name being checked: {settings.API_KEY_NAME}")
    logger.debug(f"Raw received API key: '{api_key}'")  # Log the full key in debug mode
    logger.debug(f"Raw expected API key: '{settings.API_KEY}'")  # Log the full key in debug mode
    logger.debug(f"Received API key length: {len(api_key) if api_key else 0}")
    logger.debug(f"Expected API key length: {len(settings.API_KEY) if settings.API_KEY else 0}")
    logger.debug(f"API key type received: {type(api_key)}")
    logger.debug(f"API key type expected: {type(settings.API_KEY)}")
    
    if not api_key:
        logger.warning("No API key provided in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key header is missing"
        )
    
    # Strip whitespace and compare
    received_key = api_key.strip() if api_key else ""
    expected_key = settings.API_KEY.strip() if settings.API_KEY else ""
    
    logger.debug(f"Stripped received key: '{received_key}'")
    logger.debug(f"Stripped expected key: '{expected_key}'")
    logger.debug(f"Keys equal after strip: {received_key == expected_key}")
    
    if received_key != expected_key:
        logger.warning("Invalid API key provided. Key mismatch details:")
        logger.warning(f"Received key: '{received_key}'")  # Log full key in warning for debugging
        logger.warning(f"Expected key: '{expected_key}'")  # Log full key in warning for debugging
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    
    logger.info("API key validation successful")
    return api_key
