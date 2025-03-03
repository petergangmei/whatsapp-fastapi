from fastapi import APIRouter, HTTPException, Depends
from app.schemas import MessageRequest, MessageResponse
from app.services import send_whatsapp_message
from app.auth import verify_api_key

router = APIRouter()

@router.post("/messages/", response_model=MessageResponse)
async def send_message(
    message: MessageRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Send a WhatsApp message to a specified number.
    """
    try:
        result = await send_whatsapp_message(message)
        return MessageResponse(
            success=True,
            message_id=result.get("message_id"),
            status="sent"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send message: {str(e)}"
        )
