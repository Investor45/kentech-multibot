"""
Core pairing logic for the Kentech Bot Pairing Application.
"""

from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from loguru import logger

from src.bots.models import Bot, BotPair, BotStatus, PairStatus, BotPairCreate
from src.bots.manager import bot_manager
from src.pairing.algorithms import PairingAlgorithm, DefaultPairingAlgorithm
from src.pairing.strategies import PairingStrategy, get_strategy


class PairingCore:
    """Core pairing functionality."""
    
    def __init__(self):
        self.active_pairs = {}
        self.algorithms = {
            "default": DefaultPairingAlgorithm(),
        }
    
    async def create_pair(self, pair_data: BotPairCreate, db: AsyncSession) -> Optional[BotPair]:
        """Create a new bot pair."""
        try:
            # Validate bots exist and are available
            primary_bot = await bot_manager.get_bot(pair_data.primary_bot_id, db)
            secondary_bot = await bot_manager.get_bot(pair_data.secondary_bot_id, db)
            
            if not primary_bot or not secondary_bot:
                logger.error("One or both bots not found")
                return None
            
            if primary_bot.status != BotStatus.ONLINE or secondary_bot.status != BotStatus.ONLINE:
                logger.error("Bots must be online to create pair")
                return None
            
            # Create the pair
            pair = BotPair(
                primary_bot_id=pair_data.primary_bot_id,
                secondary_bot_id=pair_data.secondary_bot_id,
                pairing_strategy=pair_data.pairing_strategy,
                status=PairStatus.ACTIVE
            )
            
            db.add(pair)
            
            # Update bot statuses
            await bot_manager.update_bot_status(pair_data.primary_bot_id, BotStatus.PAIRED, db)
            await bot_manager.update_bot_status(pair_data.secondary_bot_id, BotStatus.PAIRED, db)
            
            await db.commit()
            await db.refresh(pair)
            
            self.active_pairs[pair.id] = pair
            logger.info(f"Bot pair created: {pair.id}")
            
            return pair
            
        except Exception as e:
            logger.error(f"Failed to create bot pair: {e}")
            await db.rollback()
            return None
    
    async def get_pair(self, pair_id: str, db: AsyncSession) -> Optional[BotPair]:
        """Get a bot pair by ID."""
        try:
            result = await db.execute(
                select(BotPair)
                .where(BotPair.id == pair_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Failed to get pair {pair_id}: {e}")
            return None
    
    async def get_all_pairs(self, db: AsyncSession) -> List[BotPair]:
        """Get all bot pairs."""
        try:
            result = await db.execute(select(BotPair))
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Failed to get all pairs: {e}")
            return []
    
    async def get_active_pairs(self, db: AsyncSession) -> List[BotPair]:
        """Get active bot pairs."""
        try:
            result = await db.execute(
                select(BotPair).where(BotPair.status == PairStatus.ACTIVE)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Failed to get active pairs: {e}")
            return []
    
    async def terminate_pair(self, pair_id: str, db: AsyncSession) -> bool:
        """Terminate a bot pair."""
        try:
            pair = await self.get_pair(pair_id, db)
            if not pair:
                return False
            
            # Update pair status
            await db.execute(
                update(BotPair)
                .where(BotPair.id == pair_id)
                .values(
                    status=PairStatus.TERMINATED,
                    terminated_at=datetime.utcnow()
                )
            )
            
            # Update bot statuses back to online
            await bot_manager.update_bot_status(pair.primary_bot_id, BotStatus.ONLINE, db)
            await bot_manager.update_bot_status(pair.secondary_bot_id, BotStatus.ONLINE, db)
            
            await db.commit()
            
            if pair_id in self.active_pairs:
                del self.active_pairs[pair_id]
            
            logger.info(f"Bot pair terminated: {pair_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to terminate pair {pair_id}: {e}")
            await db.rollback()
            return False
    
    async def auto_pair_bots(self, db: AsyncSession, strategy: str = "default") -> List[BotPair]:
        """Automatically pair available bots."""
        try:
            available_bots = await bot_manager.get_available_bots(db)
            
            if len(available_bots) < 2:
                logger.info("Not enough bots available for pairing")
                return []
            
            algorithm = self.algorithms.get(strategy, self.algorithms["default"])
            pairs = algorithm.pair_bots(available_bots)
            
            created_pairs = []
            for primary_bot, secondary_bot in pairs:
                pair_data = BotPairCreate(
                    primary_bot_id=primary_bot.id,
                    secondary_bot_id=secondary_bot.id,
                    pairing_strategy=strategy
                )
                
                pair = await self.create_pair(pair_data, db)
                if pair:
                    created_pairs.append(pair)
            
            logger.info(f"Auto-paired {len(created_pairs)} bot pairs")
            return created_pairs
            
        except Exception as e:
            logger.error(f"Failed to auto-pair bots: {e}")
            return []


# Global pairing core instance
pairing_core = PairingCore()
