# Backend - Android Agent Platform

Python FastAPI backend для управления Android устройствами и автоматизации WhatsApp.

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and fill in your API keys
nano .env  # or use your favorite editor
```

**Required API keys:**
- `NOTION_API_KEY` - Your Notion integration API key
- `NOTION_DATABASE_ID` - Your WhatsApp_Outreach database ID
- `TELEGRAM_BOT_TOKEN` - Already filled (7695092594:AAFc0_3gPhzRJLNN49jtDcDbdzWWRLdfPjs)
- `TELEGRAM_CHAT_ID` - Your Telegram chat ID
- `PUTER_API_KEY` - Your Puter.js API key

### 4. Initialize Database

```bash
python scripts/init_db.py
```

This will create SQLite database at `backend/data/sqlite.db` with tables:
- `devices` - Google Pixel devices
- `tasks` - WhatsApp/LinkedIn/Instagram tasks
- `logs` - Action logs

### 5. Test ADB Connection (Optional)

```bash
python scripts/test_connection.py
```

This will load device configuration from `/config/devices.yaml` and verify setup.

### 6. Run Backend Server

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at:
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── src/
│   ├── main.py                    # FastAPI entry point
│   ├── config.py                  # Configuration management
│   ├── device_manager/            # Device control (ADB, health monitoring)
│   ├── agents/                    # WhatsApp/LinkedIn/Instagram agents
│   ├── behaviors/                 # Human behavior emulation
│   ├── integrations/              # Notion, Telegram, Puter.js
│   ├── orchestration/             # Queue, scheduler, scenarios
│   ├── database/                  # ORM models, schemas, CRUD
│   ├── routes/                    # API endpoints
│   ├── websocket/                 # Real-time WebSocket manager
│   └── utils/                     # Logger, helpers
├── scripts/
│   ├── init_db.py                 # Initialize database
│   └── test_connection.py         # Test ADB connections
├── tests/                         # Unit & integration tests
├── data/                          # SQLite database (gitignored)
├── logs/                          # Application logs (gitignored)
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (gitignored)
└── .env.example                   # Example env file
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_device_manager.py
```

## 📝 Development

### Adding New Dependencies

```bash
pip install package-name
pip freeze > requirements.txt
```

### Database Migrations

When you modify ORM models:

```bash
# Re-initialize database (WARNING: deletes all data)
python scripts/init_db.py
```

For production, use Alembic migrations (to be implemented).

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'src'"

Make sure you're running commands from the `backend/` directory and your virtual environment is activated.

### "No such file or directory: '.env'"

Copy `.env.example` to `.env` and fill in your API keys.

### Database Connection Error

Check that `backend/data/` directory exists and has write permissions.

## 📚 API Documentation

Once the server is running, visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

### Main Endpoints

- `GET /api/health` - Health check
- `GET /api/devices` - List all devices
- `GET /api/devices/{id}/status` - Get device status
- `GET /api/tasks` - List tasks
- `POST /api/tasks/sync-notion` - Sync tasks from Notion
- `POST /api/tasks/run` - Run a task
- `GET /api/logs` - Get logs (with filtering)

## 🔐 Security Notes

- Never commit `.env` file
- Keep API keys secure
- Use HTTPS in production
- Enable authentication for production deployment

## 📞 Support

For issues, check [PROGRESS.md](../PROGRESS.md) and [ROADMAP.md](../ROADMAP.md) in project root.
