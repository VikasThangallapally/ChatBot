from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import predict, chat, auth, status
from app.utils.logger import get_logger
from app.db import init_collections, close_mongo_connection
from app.config import settings
import sys
import os
from pathlib import Path

def _log_startup_info():
    try:
        logger.info(f"Python version: {sys.version}")
    except Exception:
        pass

logger = get_logger(__name__)

app = FastAPI(
    title="Brain Tumor Chatbot",
    description="AI-powered chatbot for brain tumor MRI image analysis and explanation",
    version="1.0.0"
)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint - redirects to API documentation."""
    return {
        "status": "running",
        "name": "NeuroAssist - Brain Tumor Chatbot",
        "description": "AI-powered chatbot for brain tumor MRI image analysis and explanation",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_check": "/health",
        "message": "Welcome to NeuroAssist! Visit /docs for interactive API documentation"
    }

# Initialize MongoDB collections on startup (non-blocking)
@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB collections and indexes (non-blocking)."""
    try:
        init_collections()
        logger.info("✅ MongoDB collections initialized")
    except Exception as e:
        logger.warning(f"⚠️  MongoDB initialization warning (will retry on first use): {e}")
        # Don't crash the app - MongoDB will connect lazily on first database operation


@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown."""
    try:
        close_mongo_connection()
        logger.info("✅ MongoDB connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing MongoDB connection: {e}")

# CORS middleware - configured from environment variables
logger.info(f"🔧 Configuring CORS with origins: {settings.CORS_ORIGINS}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"✅ CORS middleware configured for origins: {settings.CORS_ORIGINS}")

# Include routers (BEFORE static files)
app.include_router(predict.router, prefix="/api", tags=["Prediction"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(status.router, prefix="", tags=["Status"])

# Health check endpoint (before static files mount)
@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "Brain Tumor Chatbot",
        "version": "1.0.0"
    }

# Mount static files for uploaded images and heatmaps
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=settings.UPLOAD_DIR), name="static")
logger.info(f"Static files mounted from {settings.UPLOAD_DIR}")

# Mount React frontend static files LAST - this must be last so it doesn't interfere with API routes
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
    logger.info(f"Frontend static files mounted from {frontend_dist}")
else:
    logger.warning(f"Frontend dist directory not found at {frontend_dist}. Only API will be available.")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
