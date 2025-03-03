from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas import (
    MessageRequest,
    MessageResponse,
    HelloWorldTemplateRequest,
    OrderConfirmTemplateRequest,
    AccountCreatedTemplateRequest
)
from app.services import send_whatsapp_message
from app.auth import verify_api_key
from app.logger import logger
from typing import Dict, Any

router = APIRouter()

@router.post(
    "/messages/hello-world",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Message sent successfully"},
        401: {"description": "Unauthorized - Missing API key"},
        403: {"description": "Forbidden - Invalid API key"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
        503: {"description": "Service Unavailable - WhatsApp API unreachable"}
    }
)
async def send_hello_world(
    message: HelloWorldTemplateRequest,
    api_key: str = Depends(verify_api_key)
) -> MessageResponse:
    """
    Send the hello_world template message.
    
    Example request:
    ```json
    {
        "to_number": "919821449581"
    }
    ```
    """
    try:
        logger.info(f"Received hello_world template request for {message.to_number}")
        response = await send_whatsapp_message(message)
        return MessageResponse(
            success=True,
            message_id=response.get("messages", [{}])[0].get("id"),
            status="sent"
        )
    except Exception as e:
        logger.error(f"Error sending hello_world template: {str(e)}")
        raise

@router.post(
    "/messages/order-confirm",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Message sent successfully"},
        401: {"description": "Unauthorized - Missing API key"},
        403: {"description": "Forbidden - Invalid API key"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
        503: {"description": "Service Unavailable - WhatsApp API unreachable"}
    }
)
async def send_order_confirm(
    message: OrderConfirmTemplateRequest,
    api_key: str = Depends(verify_api_key)
) -> MessageResponse:
    """
    Send the order confirmation template with PDF attachment.
    
    The template includes:
    - A PDF document in the header
    - Body text: "Thank you for using your {card_type} card at {merchant_name}. Your {document_type} is attached as a PDF."
    
    Example request:
    ```json
    {
        "to_number": "919821449581",
        "card_type": "Credit",
        "merchant_name": "Amazon",
        "document_type": "statement",
        "pdf_url": "https://example.com/documents/statement.pdf"
    }
    ```
    """
    try:
        logger.info(f"Received order confirmation template request for {message.to_number}")
        response = await send_whatsapp_message(message)
        return MessageResponse(
            success=True,
            message_id=response.get("messages", [{}])[0].get("id"),
            status="sent"
        )
    except Exception as e:
        logger.error(f"Error sending order confirmation template: {str(e)}")
        raise

@router.post(
    "/messages/account-created",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Message sent successfully"},
        401: {"description": "Unauthorized - Missing API key"},
        403: {"description": "Forbidden - Invalid API key"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
        503: {"description": "Service Unavailable - WhatsApp API unreachable"}
    }
)
async def send_account_created(
    message: AccountCreatedTemplateRequest,
    api_key: str = Depends(verify_api_key)
) -> MessageResponse:
    """
    Send the account created template.
    
    Example request:
    ```json
    {
        "to_number": "919821449581",
        "name": "John Doe",
        "verification_type": "email"
    }
    ```
    """
    try:
        logger.info(f"Received account created template request for {message.to_number}")
        response = await send_whatsapp_message(message)
        return MessageResponse(
            success=True,
            message_id=response.get("messages", [{}])[0].get("id"),
            status="sent"
        )
    except Exception as e:
        logger.error(f"Error sending account created template: {str(e)}")
        raise

# Keep the generic endpoint for backward compatibility
@router.post(
    "/messages/",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Message sent successfully"},
        401: {"description": "Unauthorized - Missing API key"},
        403: {"description": "Forbidden - Invalid API key"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
        503: {"description": "Service Unavailable - WhatsApp API unreachable"}
    }
)
async def send_message(
    message: MessageRequest,
    api_key: str = Depends(verify_api_key)
) -> MessageResponse:
    """
    Send a generic template message.
    
    Example request:
    ```json
    {
        "to_number": "919821449581",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    ```
    """
    try:
        logger.info(f"Received message request for {message.to_number}")
        response = await send_whatsapp_message(message)
        return MessageResponse(
            success=True,
            message_id=response.get("messages", [{}])[0].get("id"),
            status="sent"
        )
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        raise
