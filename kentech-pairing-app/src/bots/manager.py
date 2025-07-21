"""
Bot management functionality.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from loguru import logger

from src.bots.models import Bot, BotStatus, BotCreate, BotUpdate
from src.config.database import get_db_session


class BotManager:
    """Manages bot lifecycle and operations."""
    
    def __init__(self):
        self.active_bots = {}
    
    async def register_bot(self, bot_data: BotCreate, db: AsyncSession) -> Bot:
        """Register a new bot."""
        try:
            bot = Bot(
                name=bot_data.name,
                bot_type=bot_data.bot_type,
                endpoint=bot_data.endpoint,
                capabilities=bot_data.capabilities,
                status=BotStatus.ONLINE
            )
            
            db.add(bot)
            await db.commit()
            await db.refresh(bot)
            
            self.active_bots[bot.id] = bot
            logger.info(f"Bot registered: {bot.name} ({bot.id})")
            
            return bot
            
        except Exception as e:
            logger.error(f"Failed to register bot: {e}")
            await db.rollback()
            raise
    
    async def get_bot(self, bot_id: str, db: AsyncSession) -> Optional[Bot]:
        """Get a bot by ID."""
        try:
            result = await db.execute(select(Bot).where(Bot.id == bot_id))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Failed to get bot {bot_id}: {e}")
            return None
    
    async def get_all_bots(self, db: AsyncSession) -> List[Bot]:
        """Get all bots."""
        try:
            result = await db.execute(select(Bot))
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Failed to get all bots: {e}")
            return []
    
    async def update_bot(self, bot_id: str, bot_data: BotUpdate, db: AsyncSession) -> Optional[Bot]:
        """Update a bot."""
        try:
            update_data = bot_data.dict(exclude_unset=True)
            update_data['updated_at'] = datetime.utcnow()
            
            await db.execute(
                update(Bot)
                .where(Bot.id == bot_id)
                .values(**update_data)
            )
            await db.commit()
            
            # Get updated bot
            return await self.get_bot(bot_id, db)
            
        except Exception as e:
            logger.error(f"Failed to update bot {bot_id}: {e}")
            await db.rollback()
            return None
    
    async def update_bot_status(self, bot_id: str, status: BotStatus, db: AsyncSession) -> bool:
        """Update bot status."""
        try:
            await db.execute(
                update(Bot)
                .where(Bot.id == bot_id)
                .values(status=status, updated_at=datetime.utcnow())
            )
            await db.commit()
            
            logger.info(f"Bot {bot_id} status updated to {status}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update bot status {bot_id}: {e}")
            await db.rollback()
            return False
    
    async def heartbeat(self, bot_id: str, db: AsyncSession) -> bool:
        """Update bot heartbeat."""
        try:
            await db.execute(
                update(Bot)
                .where(Bot.id == bot_id)
                .values(last_heartbeat=datetime.utcnow())
            )
            await db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update heartbeat for bot {bot_id}: {e}")
            await db.rollback()
            return False
    
    async def get_available_bots(self, db: AsyncSession) -> List[Bot]:
        """Get bots available for pairing."""
        try:
            result = await db.execute(
                select(Bot).where(Bot.status == BotStatus.ONLINE)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Failed to get available bots: {e}")
            return []
    
    async def deregister_bot(self, bot_id: str, db: AsyncSession) -> bool:
        """Deregister a bot."""
        try:
            await self.update_bot_status(bot_id, BotStatus.OFFLINE, db)
            
            if bot_id in self.active_bots:
                del self.active_bots[bot_id]
            
            logger.info(f"Bot deregistered: {bot_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to deregister bot {bot_id}: {e}")
            return False


# Global bot manager instance
bot_manager = BotManager()
