import httpx
from app.config import settings
from app.schemas import MessageRequest

async def send_whatsapp_message(message: MessageRequest) -> dict:
    """
    Send a message using the WhatsApp Business API.
    
    Args:
        message (MessageRequest): The message request containing recipient and content
        
    Returns:
        dict: Response from WhatsApp API
        
    Raises:
        Exception: If the API request fails
    """
    url = f"https://graph.facebook.com/v12.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": message.to_number,
        "type": message.message_type,
        "text": {"body": message.message}
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"WhatsApp API request failed: {response.text}")
            
        return response.json()
