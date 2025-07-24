import os
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    discord_webhook_url: str
    statuspage_webhook_secret: Optional[str] = None
    port: int = 8000
    log_level: str = "INFO"
    
    @field_validator('discord_webhook_url')
    @classmethod
    def validate_discord_url(cls, v):
        if not v.startswith('https://discord.com/api/webhooks/'):
            raise ValueError('Invalid Discord webhook URL')
        return v
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


settings = Settings()