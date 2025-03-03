import re
from typing import Optional

def validate_phone_number(phone_number: str) -> bool:
    """
    Validate phone number format.
    Accepts numbers with or without + prefix.
    
    Args:
        phone_number: Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Remove any whitespace
    phone_number = phone_number.strip()
    
    # Add + prefix if not present
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    
    # Basic international phone number pattern
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
