import re
from typing import Optional

def validate_phone_number(phone_number: str) -> bool:
    """
    Validate phone number format.
    Expected format: International format with country code (e.g., +1234567890)
    
    Args:
        phone_number: Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^\+[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone_number))

def validate_message_content(message: str) -> tuple[bool, Optional[str]]:
    """
    Validate message content.
    
    Args:
        message: Message content to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not message:
        return False, "Message content cannot be empty"
    
    if len(message) > 4096:  # WhatsApp message length limit
        return False, "Message content exceeds maximum length of 4096 characters"
    
    return True, None

def sanitize_message(message: str) -> str:
    """
    Sanitize message content to prevent injection attacks.
    
    Args:
        message: Message content to sanitize
        
    Returns:
        str: Sanitized message
    """
    # Remove any control characters
    message = ''.join(char for char in message if ord(char) >= 32)
    
    # Basic HTML escape (you might want to use a more comprehensive solution)
    message = message.replace('<', '&lt;').replace('>', '&gt;')
    
    return message.strip()
