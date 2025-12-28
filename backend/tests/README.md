# Testing Infrastructure - Android Agent Platform

## 📋 Overview

This directory contains the test suite for the Android Agent Platform backend. Tests are organized into three categories:

- **`unit/`** - Fast, isolated tests with no external dependencies
- **`integration/`** - Tests that use database and external services
- **`e2e/`** - End-to-end tests validating complete workflows

## 🚀 Quick Start

### 1. Install Dependencies

Ensure you have the Python virtual environment set up:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Install additional test dependencies:

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

### 2. Run All Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test categories
pytest -m unit           # Only unit tests (fast)
pytest -m integration    # Only integration tests
pytest -m e2e           # Only end-to-end tests
```

### 3. Run Specific Test Files

```bash
# Run phone validation tests
pytest tests/unit/test_whatsapp_agent.py -v

# Run API integration tests
pytest tests/integration/test_api_tasks.py -v
```

## 📊 Test Markers

Tests are marked with pytest markers for easy filtering:

- `@pytest.mark.unit` - Unit tests (fast, no external deps)
- `@pytest.mark.integration` - Integration tests (use database/APIs)
- `@pytest.mark.e2e` - End-to-end tests (full system)
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.adb` - Tests requiring ADB connection
- `@pytest.mark.llm` - Tests requiring LLM API
- `@pytest.mark.notion` - Tests requiring Notion API
- `@pytest.mark.telegram` - Tests requiring Telegram API

### Examples

```bash
# Run only fast unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"

# Run tests that don't require external services
pytest -m "not (llm or notion or telegram)"

# Run only ADB-related tests
pytest -m adb
```

## 🛠️ Available Fixtures

### Database Fixtures
- `test_db_engine` - In-memory SQLite engine
- `test_db_session` - Test database session with auto-rollback
- `seed_devices` - Seed test database with sample devices
- `seed_tasks` - Seed test database with sample tasks
- `seed_logs` - Seed test database with sample logs

### Mock Fixtures
- `mock_adb_handler` - Mock ADB operations
- `mock_llm_client` - Mock Puter.js LLM API
- `mock_notion_client` - Mock Notion API
- `mock_telegram_bot` - Mock Telegram Bot API
- `mock_websocket_manager` - Mock WebSocket connections

### Data Fixtures
- `sample_device_data` - Sample device dict
- `sample_task_data` - Sample task dict
- `sample_log_data` - Sample log dict

### Configuration Fixtures
- `test_settings` - Test configuration settings
- `async_test_client` - Async HTTP client for API testing

## 📝 Writing Tests

### Unit Test Example

```python
import pytest
from src.agents.whatsapp_agent import validate_phone_number

@pytest.mark.unit
def test_phone_validation():
    """Test phone number validation."""
    assert validate_phone_number("+66812345678") is True
    assert validate_phone_number("invalid") is False
```

### Integration Test Example

```python
import pytest

@pytest.mark.integration
async def test_sync_notion_tasks(test_db_session, mock_notion_client):
    """Test Notion task synchronization with database."""
    # Arrange
    mock_notion_client.get_pending_tasks.return_value = [...]

    # Act
    result = await sync_tasks(mock_notion_client, test_db_session)

    # Assert
    assert result["tasks_synced"] == 2
```

### Using Fixtures

```python
@pytest.mark.integration
def test_device_creation(test_db_session, sample_device_data):
    """Test creating a device in the database."""
    device = Device(**sample_device_data)
    test_db_session.add(device)
    test_db_session.commit()

    assert device.id == sample_device_data["id"]
```

## 📈 Coverage Reports

After running tests with coverage:

```bash
pytest --cov=src --cov-report=html
```

Open the HTML report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

**Coverage Goals:**
- **Unit tests:** Aim for 80%+ coverage
- **Overall:** Target 70%+ coverage

## 🔍 Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Fast, isolated tests
│   ├── test_whatsapp_agent.py
│   ├── test_device_manager.py
│   ├── test_human_behaviors.py
│   └── ...
├── integration/             # Tests with external dependencies
│   ├── test_api_tasks.py
│   ├── test_api_devices.py
│   ├── test_database.py
│   └── ...
└── e2e/                     # Full system tests
    ├── test_whatsapp_flow.py
    └── ...
```

## ⚡ Running Tests During Development

### Watch Mode (Re-run on file changes)

```bash
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw -- -v
```

### Running Specific Tests

```bash
# Run specific test class
pytest tests/unit/test_whatsapp_agent.py::TestPhoneNumberValidation -v

# Run specific test method
pytest tests/unit/test_whatsapp_agent.py::TestPhoneNumberValidation::test_valid_international_format -v
```

### Debugging Tests

```bash
# Show print statements
pytest -s

# Stop at first failure
pytest -x

# Show local variables on failure
pytest -l

# Run with pdb on failure
pytest --pdb
```

## 🚨 Common Issues

### Issue: "ModuleNotFoundError"
**Solution:** Ensure you're in the virtual environment and PYTHONPATH is set:
```bash
export PYTHONPATH="${PYTHONPATH}:/Users/admin/Desktop/Разработки/KUX/backend"
```

### Issue: "No tests found"
**Solution:** Ensure test files start with `test_` and test functions start with `test_`:
```bash
pytest --collect-only  # See what tests pytest discovers
```

### Issue: "Database locked"
**Solution:** Tests use in-memory SQLite by default. If using file-based DB, ensure proper cleanup:
```python
@pytest.fixture(autouse=True)
def cleanup_db():
    yield
    # Clean up after test
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

## 🎯 Current Status

### Implemented Tests
✅ Phone number validation unit tests (11 test cases)

### Pending Tests (After E2E Validation)
- WhatsApp Agent full message sending flow
- Device Manager tests
- Human Behavior emulation tests
- API endpoint integration tests
- Database operations tests
- WebSocket communication tests

**Note:** Many integration and E2E tests are marked as "skip" until E2E testing validates the system behavior. Once E2E testing is complete, we'll implement comprehensive test coverage for all components.

---

*Testing Infrastructure Ready | Phase 3 Foundation Complete*
