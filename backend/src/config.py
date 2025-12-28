"""Configuration management"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = Field(default="Android Agent Platform")
    app_env: str = Field(default="development")
    debug: bool = Field(default=True)
    log_level: str = Field(default="INFO")
    cors_origins: str = Field(default="http://localhost:3000")

    # Notion API
    notion_api_key: str = Field(default="test_key")
    notion_database_id: str = Field(default="test_db")

    # Telegram Bot
    telegram_bot_token: str = Field(default="test_token")
    telegram_chat_id: str = Field(default="123456789")

    # Puter.js LLM API (legacy - kept for fallback)
    puter_api_key: str = Field(default="test_puter_key")
    puter_api_url: str = Field(default="https://api.puter.ai/v1")
    puter_default_model: str = Field(default="claude-sonnet-4.5")

    # LLM via OpenRouter API (primary)
    openrouter_api_key: str = Field(default="")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1")
    llm_model: str = Field(default="google/gemini-2.0-flash-exp:free")
    llm_vision_model: str = Field(default="google/gemini-2.0-flash-exp:free")
    llm_timeout: int = Field(default=60)  # seconds
    llm_context_dir: str = Field(default="data/context")  # .md files for context

    # Database
    database_url: str = Field(default="sqlite:///./data/app.db")

    # Device Configuration
    device_config_path: str = Field(default="config/devices.yaml")

    # ADB / Tailscale
    adb_host: str = Field(default="localhost")
    adb_port: int = Field(default=5037)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
