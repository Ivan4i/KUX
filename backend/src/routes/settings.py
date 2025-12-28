"""Settings API Routes"""

import os
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger
from dotenv import load_dotenv, set_key

router = APIRouter(prefix="/api/settings", tags=["settings"])

# Get the .env file path
ENV_PATH = Path(__file__).parent.parent.parent / ".env"


class IntegrationSettings(BaseModel):
    """Integration settings model"""
    # Notion
    notion_api_key: Optional[str] = None
    notion_database_id: Optional[str] = None
    # Telegram
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    # Puter.js LLM
    puter_api_key: Optional[str] = None
    puter_api_url: Optional[str] = None
    puter_default_model: Optional[str] = None


class BehaviorSettings(BaseModel):
    """Behavior settings model"""
    # Human-like delays
    min_typing_delay_ms: int = 50
    max_typing_delay_ms: int = 150
    min_action_delay_ms: int = 500
    max_action_delay_ms: int = 2000
    # Typo simulation
    typo_probability: float = 0.03
    typo_fix_probability: float = 0.8
    # Session limits
    max_messages_per_hour: int = 20
    max_messages_per_day: int = 100
    cooldown_after_batch_min: int = 30


class AppSettings(BaseModel):
    """Application settings model"""
    app_env: str = "development"
    app_debug: bool = True
    log_level: str = "INFO"


class AllSettings(BaseModel):
    """Combined settings response"""
    integrations: IntegrationSettings
    behavior: BehaviorSettings
    app: AppSettings


def mask_secret(value: Optional[str]) -> Optional[str]:
    """Mask secret values for display"""
    if not value or len(value) < 8:
        return None
    return f"{value[:4]}...{value[-4:]}"


def get_env_value(key: str, default: str = "") -> str:
    """Get environment variable value"""
    load_dotenv(ENV_PATH)
    return os.getenv(key, default)


def set_env_value(key: str, value: str) -> bool:
    """Set environment variable in .env file"""
    try:
        # Create .env file if it doesn't exist
        if not ENV_PATH.exists():
            ENV_PATH.touch()

        set_key(str(ENV_PATH), key, value)
        return True
    except Exception as e:
        logger.error(f"Failed to set env value {key}: {e}")
        return False


@router.get(
    "/",
    response_model=AllSettings,
    summary="Get all settings",
    description="Retrieve all configuration settings (secrets are masked)"
)
async def get_all_settings():
    """
    Get all application settings

    Returns configuration for integrations, behavior, and app settings.
    Sensitive values like API keys are masked for security.
    """
    try:
        load_dotenv(ENV_PATH)

        return AllSettings(
            integrations=IntegrationSettings(
                notion_api_key=mask_secret(os.getenv("NOTION_API_KEY")),
                notion_database_id=mask_secret(os.getenv("NOTION_DATABASE_ID")),
                telegram_bot_token=mask_secret(os.getenv("TELEGRAM_BOT_TOKEN")),
                telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
                puter_api_key=mask_secret(os.getenv("PUTER_API_KEY")),
                puter_api_url=os.getenv("PUTER_API_URL", "https://api.puter.ai/v1"),
                puter_default_model=os.getenv("PUTER_DEFAULT_MODEL", "claude-sonnet-4.5"),
            ),
            behavior=BehaviorSettings(
                min_typing_delay_ms=int(os.getenv("MIN_TYPING_DELAY_MS", "50")),
                max_typing_delay_ms=int(os.getenv("MAX_TYPING_DELAY_MS", "150")),
                min_action_delay_ms=int(os.getenv("MIN_ACTION_DELAY_MS", "500")),
                max_action_delay_ms=int(os.getenv("MAX_ACTION_DELAY_MS", "2000")),
                typo_probability=float(os.getenv("TYPO_PROBABILITY", "0.03")),
                typo_fix_probability=float(os.getenv("TYPO_FIX_PROBABILITY", "0.8")),
                max_messages_per_hour=int(os.getenv("MAX_MESSAGES_PER_HOUR", "20")),
                max_messages_per_day=int(os.getenv("MAX_MESSAGES_PER_DAY", "100")),
                cooldown_after_batch_min=int(os.getenv("COOLDOWN_AFTER_BATCH_MIN", "30")),
            ),
            app=AppSettings(
                app_env=os.getenv("APP_ENV", "development"),
                app_debug=os.getenv("APP_DEBUG", "true").lower() == "true",
                log_level=os.getenv("LOG_LEVEL", "INFO"),
            )
        )
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/integrations",
    summary="Update integration settings",
    description="Update API keys and integration configuration"
)
async def update_integration_settings(settings: IntegrationSettings):
    """
    Update integration settings (Notion, Telegram, Puter.js)

    Only non-None values will be updated.
    """
    try:
        updated = []

        if settings.notion_api_key and not settings.notion_api_key.endswith("..."):
            set_env_value("NOTION_API_KEY", settings.notion_api_key)
            updated.append("NOTION_API_KEY")

        if settings.notion_database_id and not settings.notion_database_id.endswith("..."):
            set_env_value("NOTION_DATABASE_ID", settings.notion_database_id)
            updated.append("NOTION_DATABASE_ID")

        if settings.telegram_bot_token and not settings.telegram_bot_token.endswith("..."):
            set_env_value("TELEGRAM_BOT_TOKEN", settings.telegram_bot_token)
            updated.append("TELEGRAM_BOT_TOKEN")

        if settings.telegram_chat_id:
            set_env_value("TELEGRAM_CHAT_ID", settings.telegram_chat_id)
            updated.append("TELEGRAM_CHAT_ID")

        if settings.puter_api_key and not settings.puter_api_key.endswith("..."):
            set_env_value("PUTER_API_KEY", settings.puter_api_key)
            updated.append("PUTER_API_KEY")

        if settings.puter_api_url:
            set_env_value("PUTER_API_URL", settings.puter_api_url)
            updated.append("PUTER_API_URL")

        if settings.puter_default_model:
            set_env_value("PUTER_DEFAULT_MODEL", settings.puter_default_model)
            updated.append("PUTER_DEFAULT_MODEL")

        logger.success(f"✅ Updated integration settings: {updated}")
        return {
            "success": True,
            "message": f"Updated {len(updated)} settings",
            "updated": updated
        }
    except Exception as e:
        logger.error(f"Error updating integration settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/behavior",
    summary="Update behavior settings",
    description="Update human-like behavior simulation settings"
)
async def update_behavior_settings(settings: BehaviorSettings):
    """
    Update behavior settings for human-like automation
    """
    try:
        set_env_value("MIN_TYPING_DELAY_MS", str(settings.min_typing_delay_ms))
        set_env_value("MAX_TYPING_DELAY_MS", str(settings.max_typing_delay_ms))
        set_env_value("MIN_ACTION_DELAY_MS", str(settings.min_action_delay_ms))
        set_env_value("MAX_ACTION_DELAY_MS", str(settings.max_action_delay_ms))
        set_env_value("TYPO_PROBABILITY", str(settings.typo_probability))
        set_env_value("TYPO_FIX_PROBABILITY", str(settings.typo_fix_probability))
        set_env_value("MAX_MESSAGES_PER_HOUR", str(settings.max_messages_per_hour))
        set_env_value("MAX_MESSAGES_PER_DAY", str(settings.max_messages_per_day))
        set_env_value("COOLDOWN_AFTER_BATCH_MIN", str(settings.cooldown_after_batch_min))

        logger.success("✅ Updated behavior settings")
        return {
            "success": True,
            "message": "Behavior settings updated"
        }
    except Exception as e:
        logger.error(f"Error updating behavior settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/app",
    summary="Update application settings",
    description="Update general application settings"
)
async def update_app_settings(settings: AppSettings):
    """
    Update application settings (environment, debug mode, log level)
    """
    try:
        set_env_value("APP_ENV", settings.app_env)
        set_env_value("APP_DEBUG", str(settings.app_debug).lower())
        set_env_value("LOG_LEVEL", settings.log_level)

        logger.success("✅ Updated app settings")
        return {
            "success": True,
            "message": "App settings updated"
        }
    except Exception as e:
        logger.error(f"Error updating app settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/test/notion",
    summary="Test Notion connection",
    description="Verify Notion API key and database access"
)
async def test_notion_connection():
    """Test Notion API connection"""
    try:
        load_dotenv(ENV_PATH)
        api_key = os.getenv("NOTION_API_KEY")
        database_id = os.getenv("NOTION_DATABASE_ID")

        if not api_key or api_key == "your_notion_api_key_here":
            return {"success": False, "message": "Notion API key not configured"}

        if not database_id or database_id == "your_whatsapp_outreach_database_id":
            return {"success": False, "message": "Notion Database ID not configured"}

        # Try to connect to Notion
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.notion.com/v1/databases/{database_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28"
                },
                timeout=10.0
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "message": "Connected to Notion successfully",
                    "database_title": data.get("title", [{}])[0].get("text", {}).get("content", "Unknown")
                }
            else:
                return {
                    "success": False,
                    "message": f"Notion API error: {response.status_code}",
                    "detail": response.text
                }

    except Exception as e:
        logger.error(f"Notion connection test failed: {e}")
        return {"success": False, "message": str(e)}


@router.post(
    "/test/telegram",
    summary="Test Telegram bot connection",
    description="Verify Telegram bot token and send test message"
)
async def test_telegram_connection():
    """Test Telegram bot connection"""
    try:
        load_dotenv(ENV_PATH)
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not bot_token or bot_token == "your_telegram_bot_token_here":
            return {"success": False, "message": "Telegram bot token not configured"}

        if not chat_id or chat_id == "your_telegram_chat_id":
            return {"success": False, "message": "Telegram chat ID not configured"}

        # Try to send test message
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "🤖 KUX Test: Telegram connection successful!",
                    "parse_mode": "HTML"
                },
                timeout=10.0
            )

            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Test message sent successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Telegram API error: {response.status_code}",
                    "detail": response.text
                }

    except Exception as e:
        logger.error(f"Telegram connection test failed: {e}")
        return {"success": False, "message": str(e)}


@router.get(
    "/status",
    summary="Get configuration status",
    description="Check which integrations are configured"
)
async def get_configuration_status():
    """
    Get status of all configuration items

    Returns which API keys and settings are configured vs missing.
    """
    try:
        load_dotenv(ENV_PATH)

        def is_configured(key: str, placeholder: str = "") -> bool:
            value = os.getenv(key)
            if not value:
                return False
            if placeholder and value == placeholder:
                return False
            return True

        return {
            "integrations": {
                "notion": {
                    "configured": is_configured("NOTION_API_KEY", "your_notion_api_key_here") and
                                  is_configured("NOTION_DATABASE_ID", "your_whatsapp_outreach_database_id"),
                    "api_key": is_configured("NOTION_API_KEY", "your_notion_api_key_here"),
                    "database_id": is_configured("NOTION_DATABASE_ID", "your_whatsapp_outreach_database_id"),
                },
                "telegram": {
                    "configured": is_configured("TELEGRAM_BOT_TOKEN", "your_telegram_bot_token_here") and
                                  is_configured("TELEGRAM_CHAT_ID", "your_telegram_chat_id"),
                    "bot_token": is_configured("TELEGRAM_BOT_TOKEN", "your_telegram_bot_token_here"),
                    "chat_id": is_configured("TELEGRAM_CHAT_ID", "your_telegram_chat_id"),
                },
                "puter": {
                    "configured": is_configured("PUTER_API_KEY", "your_puter_api_key_here"),
                    "api_key": is_configured("PUTER_API_KEY", "your_puter_api_key_here"),
                }
            },
            "env_file_exists": ENV_PATH.exists()
        }
    except Exception as e:
        logger.error(f"Error getting config status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
