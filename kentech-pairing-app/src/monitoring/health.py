"""
Health check endpoints and monitoring.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.config.database import get_db_session
from src.config.settings import get_settings

health_router = APIRouter()


@health_router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "kentech-bot-pairing",
        "version": "1.0.0"
    }


@health_router.get("/health/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db_session)):
    """Detailed health check with database connectivity."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "kentech-bot-pairing",
        "version": "1.0.0",
        "checks": {}
    }
    
    # Check database connectivity
    try:
        await db.execute("SELECT 1")
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}"
        }
    
    # Check configuration
    try:
        settings = get_settings()
        health_status["checks"]["config"] = {
            "status": "healthy",
            "message": "Configuration loaded successfully",
            "debug_mode": settings.debug
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["config"] = {
            "status": "unhealthy",
            "message": f"Configuration error: {str(e)}"
        }
    
    return health_status


@health_router.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db_session)):
    """Kubernetes readiness probe endpoint."""
    try:
        # Check if we can query the database
        await db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}, 503


@health_router.get("/health/live")
async def liveness_check():
    """Kubernetes liveness probe endpoint."""
    return {"status": "alive"}
