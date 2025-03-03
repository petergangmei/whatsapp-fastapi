from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Union

class TemplateLanguage(BaseModel):
    code: str = "en_US"

class TemplateParameter(BaseModel):
    type: str
    text: Optional[str] = None
    document: Optional[HttpUrl] = None

class TemplateComponent(BaseModel):
    type: str  # "header" or "body"
    parameters: List[TemplateParameter]

class Template(BaseModel):
    name: str
    language: TemplateLanguage
    components: Optional[List[TemplateComponent]] = None

# Specific template request models for better type safety and validation
class HelloWorldTemplateRequest(BaseModel):
    """Request model for hello_world template"""
    to_number: str
    template_name: str = "hello_world"

class OrderConfirmTemplateRequest(BaseModel):
    """Request model for order confirmation template with PDF header"""
    to_number: str
    template_name: str = "order_confirm"
    card_type: str
    merchant_name: str
    document_type: str
    pdf_url: HttpUrl = Field(..., description="URL to the PDF document that will be attached in the header")

class AccountCreatedTemplateRequest(BaseModel):
    """Request model for account creation template"""
    to_number: str
    template_name: str = "account_created"
    name: str
    verification_type: str  # e.g., "email", "phone number"

# Generic message request that can handle any template
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
