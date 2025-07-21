"""
Database initialization script for Kentech Bot Pairing Application.
Run this to create the database tables.
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config.database import init_database
from loguru import logger


async def main():
    """Initialize the database."""
    try:
        logger.info("Initializing database tables...")
        await init_database()
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("🗄️ Initializing Kentech Bot Pairing Database...")
    success = asyncio.run(main())
    
    if success:
        print("✅ Database initialized successfully!")
        print("🚀 You can now start the application with: python run_app.py")
    else:
        print("❌ Database initialization failed!")
        print("🔧 Check the logs for more details.")
