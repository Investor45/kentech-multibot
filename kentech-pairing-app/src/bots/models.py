"""
Database models for bots and bot pairs.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import String, DateTime, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel, Field

from src.config.database import Base


class BotStatus(str, Enum):
    """Bot status enumeration."""
    OFFLINE = "offline"
    ONLINE = "online"
    PAIRED = "paired"
    BUSY = "busy"
    ERROR = "error"


class PairStatus(str, Enum):
    """Pair status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"


class Bot(Base):
    """Bot database model."""
    __tablename__ = "bots"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bot_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[BotStatus] = mapped_column(String(20), default=BotStatus.OFFLINE)
    endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    capabilities: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_heartbeat: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pairs_as_primary = relationship("BotPair", foreign_keys="BotPair.primary_bot_id", back_populates="primary_bot")
    pairs_as_secondary = relationship("BotPair", foreign_keys="BotPair.secondary_bot_id", back_populates="secondary_bot")


class BotPair(Base):
    """Bot pair database model."""
    __tablename__ = "bot_pairs"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    primary_bot_id: Mapped[str] = mapped_column(String(36), ForeignKey("bots.id"), nullable=False)
    secondary_bot_id: Mapped[str] = mapped_column(String(36), ForeignKey("bots.id"), nullable=False)
    status: Mapped[PairStatus] = mapped_column(String(20), default=PairStatus.ACTIVE)
    pairing_strategy: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    terminated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    primary_bot = relationship("Bot", foreign_keys=[primary_bot_id], back_populates="pairs_as_primary")
    secondary_bot = relationship("Bot", foreign_keys=[secondary_bot_id], back_populates="pairs_as_secondary")


# Pydantic models for API serialization
class BotCreate(BaseModel):
    """Bot creation model."""
    name: str = Field(..., min_length=1, max_length=100)
    bot_type: str = Field(..., min_length=1, max_length=50)
    endpoint: str = Field(..., min_length=1, max_length=255)
    capabilities: Optional[str] = None


class BotUpdate(BaseModel):
    """Bot update model."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[BotStatus] = None
    endpoint: Optional[str] = Field(None, min_length=1, max_length=255)
    capabilities: Optional[str] = None


class BotResponse(BaseModel):
    """Bot response model."""
    id: str
    name: str
    bot_type: str
    status: BotStatus
    endpoint: str
    capabilities: Optional[str]
    last_heartbeat: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BotPairCreate(BaseModel):
    """Bot pair creation model."""
    primary_bot_id: str
    secondary_bot_id: str
    pairing_strategy: str = "default"


class BotPairResponse(BaseModel):
    """Bot pair response model."""
    id: str
    primary_bot_id: str
    secondary_bot_id: str
    status: PairStatus
    pairing_strategy: str
    created_at: datetime
    terminated_at: Optional[datetime]
    primary_bot: BotResponse
    secondary_bot: BotResponse
    
    class Config:
        from_attributes = True
