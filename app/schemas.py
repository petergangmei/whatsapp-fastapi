from pydantic import BaseModel, Field
from typing import Optional

class TemplateLanguage(BaseModel):
    code: str = "en_US"

class Template(BaseModel):
    name: str
    language: TemplateLanguage

class MessageRequest(BaseModel):
    """
    Schema for WhatsApp message request
    """
    to_number: str
    message_type: str = "template"  # Default to template type
    template: Template
    message: Optional[str] = None  # Keep this for backward compatibility

class MessageResponse(BaseModel):
    """Schema for message response."""
    success: bool = Field(..., description="Whether the message was sent successfully")
    message_id: Optional[str] = Field(None, description="WhatsApp message ID if successful")
    status: str = Field(..., description="Status of the message (sent, failed, etc.)")
    error: Optional[str] = Field(None, description="Error message if any")
