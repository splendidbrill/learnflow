"""
LearnAI Backend - Main Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="LearnAI API",
    version="1.0.0",
    description="AI-powered personalized learning platform"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from routers import book_router, explain_router, chat_router, pattern_router

# Register routers
app.include_router(book_router.router, prefix="/api/books", tags=["Books"])
app.include_router(explain_router.router, prefix="/api/explain", tags=["Explanations"])
app.include_router(chat_router.router, prefix="/api/chat", tags=["Chat"])
app.include_router(pattern_router.router, prefix="/api/patterns", tags=["Patterns"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "LearnAI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from config import settings
    
    return {
        "status": "healthy",
        "anthropic_configured": bool(settings.ANTHROPIC_API_KEY),
        "supabase_configured": bool(settings.SUPABASE_URL)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)