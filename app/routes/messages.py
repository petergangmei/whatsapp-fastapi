from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas import MessageRequest, MessageResponse
from app.services import send_whatsapp_message
from app.auth import verify_api_key
from app.logger import logger
from typing import Dict, Any

router = APIRouter()

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
    Send a WhatsApp message to a specified number.
    
    Args:
        message: The message request containing recipient and content
        api_key: API key for authentication (injected by FastAPI)
        
    Returns:
        MessageResponse: The response containing success status and message details
        
    Raises:
        HTTPException: If message sending fails or validation fails
    """
    try:
        logger.info(f"Received message request for {message.to_number}")
        result = await send_whatsapp_message(message)
        
        response = MessageResponse(
            success=True,
            message_id=result.get("messages", [{}])[0].get("id"),
            status="sent"
        )
        
        logger.info(f"Successfully processed message request for {message.to_number}")
        return response
        
    except HTTPException as he:
        # Re-raise HTTP exceptions from the service layer
        logger.error(f"HTTP error while sending message: {he.detail}")
        raise
        
    except Exception as e:
        # Log unexpected errors and return a generic error message
        logger.error(f"Unexpected error while processing message request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request"
        )
