"""Main FastAPI application using Supabase REST API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    users_supabase as users,
    goals_supabase as goals,
    plans_supabase as plans,
    milestones_supabase as milestones,
    checkins_supabase as checkins,
    conversations_supabase as conversations
)
from app.config import get_settings

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="AI Personal Coach API",
    description="Backend API for AI-powered personal coaching agent (Supabase Edition)",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - adjust for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(goals.router)
app.include_router(plans.router)
app.include_router(milestones.router)
app.include_router(checkins.router)
app.include_router(conversations.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "AI Personal Coach API (Supabase Edition)",
        "version": "2.0.0",
        "docs": "/docs",
        "status": "running",
        "database": "Supabase REST API"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "database": "Supabase REST API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
