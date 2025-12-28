"""
Pytest configuration and fixtures for Android Agent Platform tests

This module provides reusable fixtures for unit, integration, and e2e tests.
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import Mock, AsyncMock, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.database import models
from src.config import Settings


# ==================== Database Fixtures ====================

@pytest.fixture(scope="function")
def test_db_engine():
    """
    Create an in-memory SQLite database engine for testing.

    Each test gets a fresh database that is destroyed after the test completes.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine) -> Generator[Session, None, None]:
    """
    Create a test database session.

    The session is automatically rolled back after each test to ensure isolation.
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


# ==================== Mock Fixtures ====================

@pytest.fixture
def mock_adb_handler():
    """Mock ADB handler for testing device operations without real devices."""
    mock = MagicMock()

    # Mock successful ADB commands
    mock.connect.return_value = True
    mock.disconnect.return_value = True
    mock.execute_command.return_value = ("success", "", 0)
    mock.get_battery_level.return_value = 85
    mock.get_device_temperature.return_value = 35.5
    mock.tap.return_value = True
    mock.swipe.return_value = True
    mock.input_text.return_value = True
    mock.screenshot.return_value = b"fake_screenshot_data"
    mock.start_app.return_value = True
    mock.reboot.return_value = True

    return mock


@pytest.fixture
def mock_llm_client():
    """Mock Puter.js LLM client for testing AI operations."""
    mock = AsyncMock()

    # Mock LLM responses
    mock.generate_message.return_value = {
        "success": True,
        "message": "Hey! How are you doing today? 😊",
        "tokens_used": 50
    }

    mock.analyze_screenshot.return_value = {
        "success": True,
        "analysis": "WhatsApp chat screen is visible",
        "ui_elements": ["chat_input", "send_button", "back_button"],
        "confidence": 0.95
    }

    mock.suggest_recovery_action.return_value = {
        "success": True,
        "action": "retry",
        "reason": "Temporary UI issue detected",
        "alternative_steps": ["tap at (500, 800)", "wait 2s", "try again"]
    }

    return mock


@pytest.fixture
def mock_notion_client():
    """Mock Notion API client for testing task synchronization."""
    mock = AsyncMock()

    # Mock Notion API responses
    mock.get_pending_tasks.return_value = [
        {
            "notion_id": "task-1",
            "recipient_name": "John Doe",
            "phone_number": "+66812345678",
            "message_content": "Hello! This is a test message.",
            "priority": 1,
            "status": "Pending"
        },
        {
            "notion_id": "task-2",
            "recipient_name": "Jane Smith",
            "phone_number": "+66898765432",
            "message_content": "Hi Jane! How are you?",
            "priority": 2,
            "status": "Pending"
        }
    ]

    mock.update_task_status.return_value = {"success": True}
    mock.batch_update_tasks.return_value = {"success": True, "updated": 2}

    return mock


@pytest.fixture
def mock_telegram_bot():
    """Mock Telegram Bot for testing notifications."""
    mock = AsyncMock()

    mock.send_alert.return_value = True
    mock.send_task_completed.return_value = True
    mock.send_device_alert.return_value = True
    mock.send_daily_summary.return_value = True

    return mock


@pytest.fixture
def mock_websocket_manager():
    """Mock WebSocket manager for testing real-time updates."""
    mock = AsyncMock()

    mock.connect.return_value = None
    mock.disconnect.return_value = None
    mock.broadcast.return_value = None
    mock.send_personal_message.return_value = None

    # Track connections
    mock.active_connections = []

    return mock


# ==================== Test Data Fixtures ====================

@pytest.fixture
def sample_device_data():
    """Sample device data for testing."""
    return {
        "id": "pixel-th-1",
        "name": "Pixel 5 - Thailand Device 1",
        "tailscale_ip": "100.64.0.1",
        "adb_port": 5555,
        "status": "online",
        "battery_level": 85,
        "temperature": 35.5,
        "memory_usage": 60,
        "active_tasks": 0,
        "last_health_check": "2025-12-04T10:00:00Z"
    }


@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        "id": 1,
        "notion_id": "task-123",
        "recipient_name": "John Doe",
        "phone_number": "+66812345678",
        "message_content": "Hello! This is a test message.",
        "priority": 1,
        "status": "Pending",
        "device_id": None,
        "attempt_count": 0,
        "error_message": None
    }


@pytest.fixture
def sample_log_data():
    """Sample log entry data for testing."""
    return {
        "id": 1,
        "device_id": "pixel-th-1",
        "task_id": 1,
        "action_type": "whatsapp_send",
        "status": "success",
        "details": "Message sent successfully to +66812345678",
        "duration_seconds": 12.5,
        "error_message": None,
        "screenshot_path": None
    }


# ==================== Database Seeding Fixtures ====================

@pytest.fixture
def seed_devices(test_db_session, sample_device_data):
    """Seed test database with sample devices."""
    device = models.Device(
        id=sample_device_data["id"],
        name=sample_device_data["name"],
        tailscale_ip=sample_device_data["tailscale_ip"],
        adb_port=sample_device_data["adb_port"],
        status=sample_device_data["status"]
    )
    test_db_session.add(device)
    test_db_session.commit()
    test_db_session.refresh(device)
    return device


@pytest.fixture
def seed_tasks(test_db_session, sample_task_data):
    """Seed test database with sample tasks."""
    task = models.Task(
        notion_id=sample_task_data["notion_id"],
        recipient_name=sample_task_data["recipient_name"],
        phone_number=sample_task_data["phone_number"],
        message_content=sample_task_data["message_content"],
        priority=sample_task_data["priority"],
        status=sample_task_data["status"]
    )
    test_db_session.add(task)
    test_db_session.commit()
    test_db_session.refresh(task)
    return task


@pytest.fixture
def seed_logs(test_db_session, sample_log_data):
    """Seed test database with sample logs."""
    log = models.Log(
        device_id=sample_log_data["device_id"],
        task_id=sample_log_data["task_id"],
        action_type=sample_log_data["action_type"],
        status=sample_log_data["status"],
        details=sample_log_data["details"],
        duration_seconds=sample_log_data["duration_seconds"]
    )
    test_db_session.add(log)
    test_db_session.commit()
    test_db_session.refresh(log)
    return log


# ==================== Configuration Fixtures ====================

@pytest.fixture
def test_settings():
    """Test configuration settings."""
    return Settings(
        # Database
        DATABASE_URL="sqlite:///:memory:",

        # API Keys (mock values for testing)
        NOTION_API_KEY="test_notion_key",
        NOTION_DATABASE_ID="test_db_id",
        TELEGRAM_BOT_TOKEN="test_bot_token",
        TELEGRAM_CHAT_ID="123456789",
        PUTER_API_KEY="test_puter_key",

        # Application settings
        APP_NAME="Android Agent Platform - Test",
        DEBUG=True,
        LOG_LEVEL="DEBUG"
    )


# ==================== Async Fixtures ====================

@pytest.fixture
async def async_test_client():
    """
    Async HTTP client for testing FastAPI endpoints.

    Note: Requires httpx to be installed: pip install httpx
    """
    # Import here to make it optional
    try:
        from httpx import AsyncClient
        from src.main import app

        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    except ImportError:
        pytest.skip("httpx not installed - install with: pip install httpx")


# ==================== Utility Functions ====================

def assert_device_status_valid(device_status: dict):
    """Assert that a device status dict has valid values."""
    assert device_status["battery_level"] >= 0
    assert device_status["battery_level"] <= 100
    assert device_status["temperature"] >= -20
    assert device_status["temperature"] <= 80
    assert device_status["memory_usage"] >= 0
    assert device_status["memory_usage"] <= 100
    assert device_status["status"] in ["online", "offline", "busy", "sleeping", "overheating", "low_battery"]


def assert_task_valid(task: dict):
    """Assert that a task dict has valid values."""
    assert task["phone_number"].startswith("+")
    assert len(task["phone_number"]) >= 8
    assert len(task["phone_number"]) <= 16
    assert task["priority"] >= 1
    assert task["priority"] <= 5
    assert task["status"] in ["Pending", "Running", "Sent", "Failed"]


def assert_log_valid(log: dict):
    """Assert that a log entry dict has valid values."""
    assert log["action_type"] in ["whatsapp_send", "device_reboot", "health_check", "screenshot"]
    assert log["status"] in ["success", "warning", "failed", "info"]
    if log["duration_seconds"] is not None:
        assert log["duration_seconds"] >= 0
        assert log["duration_seconds"] <= 3600


# ==================== Pytest Hooks ====================

def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast, no external dependencies)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (may use database, external services)"
    )
    config.addinivalue_line(
        "markers", "e2e: End-to-end tests (full system tests)"
    )
