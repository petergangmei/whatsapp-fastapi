from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import messages
from app.config import settings
from app.middleware.security import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    HTTPSRedirectMiddleware
)

# Initialize FastAPI application
app = FastAPI(
    title="WhatsApp Microservice",
    description="A microservice for handling WhatsApp messaging operations",
    version="1.0.0"
)

# Add security middleware
if settings.ENFORCE_HTTPS:
    app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(SecurityHeadersMiddleware)

# Add rate limiting
app.add_middleware(
    RateLimitMiddleware,
    max_requests=settings.RATE_LIMIT_MAX_REQUESTS,
    window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Include routers
app.include_router(messages.router, prefix="/api/v1", tags=["messages"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "WhatsApp Microservice API",
        "status": "active",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
