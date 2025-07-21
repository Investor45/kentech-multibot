"""
Kentech Bot Pairing Application
Main entry point for the bot pairing system.
"""

import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from loguru import logger

from src.config.settings import get_settings
from src.api.routes import router as api_router
from src.api.websockets import websocket_router
from src.config.database import init_database
from src.monitoring.health import health_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="Kentech Bot Pairing API",
        description="API for managing and pairing bots in the Kentech ecosystem",
        version="1.0.0",
        debug=settings.debug
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(api_router, prefix="/api")
    app.include_router(websocket_router, prefix="/ws")
    app.include_router(health_router, prefix="/health")
    
    # Serve static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Serve the main page
    @app.get("/")
    async def read_root():
        return FileResponse("static/index.html")
    
    return app


async def startup():
    """Application startup tasks."""
    logger.info("Starting Kentech Bot Pairing Application...")
    
    # Initialize database
    try:
        await init_database()
        logger.info("Database initialization completed successfully!")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # Don't raise the error to prevent startup failure
    
    logger.info("Application started successfully!")


async def shutdown():
    """Application shutdown tasks."""
    logger.info("Shutting down Kentech Bot Pairing Application...")


def main():
    """Main entry point."""
    settings = get_settings()
    
    # Configure logging
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        level=settings.log_level
    )
    
    global app
    app = create_app()
    
    # Add startup and shutdown events
    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


# Create app instance for uvicorn
app = create_app()


if __name__ == "__main__":
    main()
