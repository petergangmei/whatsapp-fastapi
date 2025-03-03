# WhatsApp Microservice

A FastAPI-based microservice for handling WhatsApp messaging operations.

## Features

- Send WhatsApp messages via API
- API Key authentication
- Input validation and sanitization
- Structured logging
- Error handling
- CORS support

## Prerequisites

- Python 3.8+
- WhatsApp Business API access
- WhatsApp API Token
- WhatsApp Phone Number ID

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd whatsapp-microservice
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```

## Configuration

Update the following variables in your `.env` file:

```env
WHATSAPP_API_TOKEN=your_whatsapp_api_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
API_KEY=your_api_key_here
```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Usage

### Send a Message

```bash
curl -X POST "http://localhost:8000/api/v1/messages/" \
     -H "X-API-Key: your_api_key_here" \
     -H "Content-Type: application/json" \
     -d '{
           "to_number": "+1234567890",
           "message": "Hello, World!",
           "message_type": "text"
         }'
```

## Security

- API Key authentication required for all endpoints
- Input validation and sanitization
- CORS configuration (customize in production)

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 200: Success
- 401: Unauthorized (missing API key)
- 403: Forbidden (invalid API key)
- 422: Validation Error
- 500: Server Error

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# whatsapp-fastapi
