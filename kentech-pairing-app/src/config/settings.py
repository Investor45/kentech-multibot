"""
Configuration management for the Kentech Bot Pairing Application.
"""

import os
from functools import lru_cache
from typing import List

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application settings
    debug: bool = False
    host: str = "localhost"
    port: int = 8000
    log_level: str = "INFO"
    
    # Database settings
    database_url: str = "sqlite+aiosqlite:///./kentech_pairing.db"
    database_echo: bool = False
    
    # Redis settings
    redis_url: str = "redis://localhost:6379/0"
    redis_password: str = ""
    
    # Security
    secret_key: str = "your-secret-key-here"
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Bot pairing settings
    max_bots_per_pair: int = 2
    pairing_timeout: int = 30
    health_check_interval: int = 60
    
    # Monitoring
    metrics_enabled: bool = True
    metrics_port: int = 9090
    
    # API settings
    api_prefix: str = "/api/v1"
    max_connections_per_ip: int = 100
    
    # WebSocket settings
    ws_heartbeat_interval: int = 30
    ws_message_max_size: int = 1024
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of: {valid_levels}')
        return v.upper()
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
