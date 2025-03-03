from pydantic import BaseModel, Field
from typing import Optional

class MessageRequest(BaseModel):
    """Schema for incoming message requests."""
    to_number: str = Field(..., description="Recipient's phone number with country code")
    message: str = Field(..., description="Message content to be sent")
    message_type: str = Field(default="text", description="Type of message (text, template, etc.)")

class MessageResponse(BaseModel):
    """Schema for message response."""
    success: bool = Field(..., description="Whether the message was sent successfully")
    message_id: Optional[str] = Field(None, description="WhatsApp message ID if successful")
    status: str = Field(..., description="Status of the message (sent, failed, etc.)")
    error: Optional[str] = Field(None, description="Error message if any")
