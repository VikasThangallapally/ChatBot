from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import predict, chat, auth, status
from app.utils.logger import get_logger
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

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Mount static files (React frontend) LAST - this must be last so it doesn't interfere with API routes
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")
    logger.info(f"Static files mounted from {frontend_dist}")
else:
    logger.warning(f"Frontend dist directory not found at {frontend_dist}. Only API will be available.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
