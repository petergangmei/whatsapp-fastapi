from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config import settings

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
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key header is missing"
        )
    
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
        
    return api_key
