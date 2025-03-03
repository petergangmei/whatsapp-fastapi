from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import messages

# Initialize FastAPI application
app = FastAPI(
    title="WhatsApp Microservice",
    description="A microservice for handling WhatsApp messaging operations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(messages.router, prefix="/api/v1", tags=["messages"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "WhatsApp Microservice API", "status": "active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
