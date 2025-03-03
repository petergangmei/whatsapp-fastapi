import httpx
from app.config import settings
from app.schemas import MessageRequest
from app.logger import logger
from app.utils.validators import validate_phone_number, validate_message_content, sanitize_message
from fastapi import HTTPException
from typing import Dict, Any

async def send_whatsapp_message(message: MessageRequest) -> Dict[str, Any]:
    """
    Send a message using the WhatsApp Business API.
    
    Args:
        message (MessageRequest): The message request containing recipient and content
        
    Returns:
        dict: Response from WhatsApp API
        
    Raises:
        HTTPException: If validation fails or API request fails
    """
    # Validate phone number
    if not validate_phone_number(message.to_number):
        logger.error(f"Invalid phone number format: {message.to_number}")
        raise HTTPException(
            status_code=422,
            detail="Invalid phone number format. Use international format (e.g., +1234567890)"
        )
    
    # Validate and sanitize message content
    is_valid, error_message = validate_message_content(message.message)
    if not is_valid:
        logger.error(f"Invalid message content: {error_message}")
        raise HTTPException(
            status_code=422,
            detail=error_message
        )
    
    sanitized_message = sanitize_message(message.message)
    
    url = f"https://graph.facebook.com/v12.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": message.to_number,
        "type": message.message_type,
        "text": {"body": sanitized_message}
    }
    
    try:
        logger.info(f"Sending WhatsApp message to {message.to_number}")
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code != 200:
                error_detail = response.json() if response.text else "No error details available"
                logger.error(f"WhatsApp API request failed: {error_detail}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"WhatsApp API request failed: {error_detail}"
                )
            
            response_data = response.json()
            logger.info(f"Successfully sent message to {message.to_number}")
            return response_data
            
    except httpx.RequestError as e:
        logger.error(f"Failed to send request: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error while sending message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while sending message"
        )
