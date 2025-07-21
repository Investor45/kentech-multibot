"""
API routes for the Kentech Bot Pairing Application.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db_session
from src.bots.models import BotCreate, BotUpdate, BotResponse, BotPairCreate, BotPairResponse
from src.bots.manager import bot_manager
from src.api.websockets import notify_pair_created, notify_pair_terminated
from src.pairing import pairing_core
from src.pairing.strategies import get_available_strategies

router = APIRouter()


# Bot endpoints
@router.post("/bots", response_model=BotResponse, status_code=status.HTTP_201_CREATED)
async def create_bot(
    bot_data: BotCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Register a new bot."""
    bot = await bot_manager.register_bot(bot_data, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register bot"
        )
    return bot


@router.get("/bots", response_model=List[BotResponse])
async def get_bots(db: AsyncSession = Depends(get_db_session)):
    """Get all registered bots."""
    return await bot_manager.get_all_bots(db)


@router.get("/bots/{bot_id}", response_model=BotResponse)
async def get_bot(
    bot_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Get a specific bot by ID."""
    bot = await bot_manager.get_bot(bot_id, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    return bot


@router.put("/bots/{bot_id}", response_model=BotResponse)
async def update_bot(
    bot_id: str,
    bot_data: BotUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """Update a bot."""
    bot = await bot_manager.update_bot(bot_id, bot_data, db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found or update failed"
        )
    return bot


@router.post("/bots/{bot_id}/heartbeat")
async def bot_heartbeat(
    bot_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Update bot heartbeat."""
    success = await bot_manager.heartbeat(bot_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    return {"message": "Heartbeat updated"}


@router.delete("/bots/{bot_id}")
async def deregister_bot(
    bot_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Deregister a bot."""
    success = await bot_manager.deregister_bot(bot_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    return {"message": "Bot deregistered"}


# Bot pair endpoints
@router.post("/pairs", response_model=BotPairResponse, status_code=status.HTTP_201_CREATED)
async def create_pair(
    pair_data: BotPairCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Create a new bot pair."""
    pair = await pairing_core.create_pair(pair_data, db)
    if not pair:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create bot pair"
        )
    
    # Notify about pair creation via WebSocket
    await notify_pair_created(pair.id, pair.primary_bot_id, pair.secondary_bot_id)
    
    return pair


@router.get("/pairs", response_model=List[BotPairResponse])
async def get_pairs(db: AsyncSession = Depends(get_db_session)):
    """Get all bot pairs."""
    return await pairing_core.get_all_pairs(db)


@router.get("/pairs/active", response_model=List[BotPairResponse])
async def get_active_pairs(db: AsyncSession = Depends(get_db_session)):
    """Get active bot pairs."""
    return await pairing_core.get_active_pairs(db)


@router.get("/pairs/{pair_id}", response_model=BotPairResponse)
async def get_pair(
    pair_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Get a specific bot pair by ID."""
    pair = await pairing_core.get_pair(pair_id, db)
    if not pair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot pair not found"
        )
    return pair


@router.delete("/pairs/{pair_id}")
async def terminate_pair(
    pair_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Terminate a bot pair."""
    # Get pair info before terminating for notifications
    pair = await pairing_core.get_pair(pair_id, db)
    if not pair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot pair not found"
        )
    
    success = await pairing_core.terminate_pair(pair_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to terminate bot pair"
        )
    
    # Notify about pair termination via WebSocket
    await notify_pair_terminated(pair.id, pair.primary_bot_id, pair.secondary_bot_id)
    
    return {"message": "Bot pair terminated"}


@router.post("/pairs/auto", response_model=List[BotPairResponse])
async def auto_pair_bots(
    strategy: str = "default",
    db: AsyncSession = Depends(get_db_session)
):
    """Automatically pair available bots."""
    pairs = await pairing_core.auto_pair_bots(db, strategy)
    return pairs


# Strategy endpoints
@router.get("/strategies")
async def get_strategies():
    """Get available pairing strategies."""
    return {"strategies": get_available_strategies()}


# Status endpoint
@router.get("/status")
async def get_status(db: AsyncSession = Depends(get_db_session)):
    """Get system status."""
    all_bots = await bot_manager.get_all_bots(db)
    active_pairs = await pairing_core.get_active_pairs(db)
    
    return {
        "total_bots": len(all_bots),
        "online_bots": len([b for b in all_bots if b.status == "online"]),
        "paired_bots": len([b for b in all_bots if b.status == "paired"]),
        "active_pairs": len(active_pairs),
        "available_strategies": get_available_strategies()
    }
