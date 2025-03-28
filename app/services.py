import httpx
from app.config import settings
from app.schemas import (
    MessageRequest, 
    HelloWorldTemplateRequest,
    OrderConfirmTemplateRequest,
    AccountCreatedTemplateRequest,
    TemplateComponent,
    TemplateParameter
)
from app.logger import logger
from app.utils.validators import validate_phone_number
from fastapi import HTTPException
from typing import Dict, Any, Union

async def send_whatsapp_message(
    message: Union[
        MessageRequest, 
        HelloWorldTemplateRequest,
        OrderConfirmTemplateRequest,
        AccountCreatedTemplateRequest
    ]
) -> Dict[str, Any]:
    """
    Send a message using the WhatsApp Business API.
    
    Args:
        message: The message request containing recipient and template info
        
    Returns:
        dict: Response from WhatsApp API
        
    Raises:
        HTTPException: If validation fails or API request fails
    """
    # Format and validate phone number
    phone_number = message.to_number.strip()
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
        
    if not validate_phone_number(phone_number):
        logger.error(f"Invalid phone number format: {phone_number}")
        raise HTTPException(
            status_code=422,
            detail="Invalid phone number format. Use international format (e.g., +1234567890)"
        )
    
    # Remove the + prefix for WhatsApp API
    phone_number = phone_number[1:] if phone_number.startswith('+') else phone_number
    
    # Construct the API URL using v12.0 as per the example
    url = f"https://graph.facebook.com/v12.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Base payload
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": getattr(message, "template_name", None) or message.template.name,
            "language": {
                "code": "en_US"
            }
        }
    }
    
    # Add template-specific components
    if isinstance(message, OrderConfirmTemplateRequest):
        # Add both header (PDF) and body components
        payload["template"]["components"] = [
            {
                "type": "header",
                "parameters": [
                    {
                        "type": "document",
                        "document": {
                            "link": str(message.pdf_url)
                        }
                    }
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": message.card_type},
                    {"type": "text", "text": message.merchant_name},
                    {"type": "text", "text": message.document_type}
                ]
            }
        ]
    elif isinstance(message, AccountCreatedTemplateRequest):
        payload["template"]["components"] = [{
            "type": "body",
            "parameters": [
                {"type": "text", "text": message.name},
                {"type": "text", "text": message.verification_type}
            ]
        }]
    elif isinstance(message, MessageRequest) and message.template.components:
        payload["template"]["components"] = message.template.components
    
    try:
        logger.info(f"Sending WhatsApp template message to {phone_number}")
        logger.debug(f"Using template: {payload['template']['name']}")
        logger.debug(f"Request payload: {payload}")
        
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
            logger.info(f"Successfully sent template message to {phone_number}")
            logger.debug(f"WhatsApp API response: {response_data}")
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
