# Android Agent Platform

Desktop приложение для автоматизации WhatsApp рассылок через удаленные Google Pixel 5 устройства, подключенные через VPN (Tailscale + ADB).

## 🚀 Быстрый Старт

### Prerequisites

- Python 3.11+
- Node.js 18+
- ADB (Android Debug Bridge)
- Tailscale VPN
- Google Pixel 5 devices (3 шт)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example and fill in your values)
cp .env.example .env

# Initialize database
python scripts/init_db.py

# Run backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

### Access

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📁 Project Structure

```
android-agent-platform/
├── backend/          # Python Backend (FastAPI)
├── frontend/         # React Frontend (TypeScript)
├── scripts/          # Utility scripts
├── config/           # Configuration files
├── docs/             # Documentation
├── ROADMAP.md        # Development roadmap
├── PROGRESS.md       # Current progress
└── README.md         # This file
```

## 📚 Documentation

- **[ROADMAP.md](ROADMAP.md)** - Full development plan (Slice 1, 2, 3)
- **[PROGRESS.md](PROGRESS.md)** - Current progress tracker
- **[IDEAL_VISION.md](IDEAL_VISION.md)** - Project vision
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Detailed implementation guide
- **[V3-DESIGN_SYSTEM.md](V3-DESIGN_SYSTEM.md)** - UI/UX design system
- **[promt-dev-base.md](promt-dev-base.md)** - Development principles

## 🎯 Current Status

**Phase:** Slice 1 - Минимальный WhatsApp Flow (MVP)

**Progress:** 0/14 tasks completed

See [PROGRESS.md](PROGRESS.md) for detailed status.

## 🔧 Tech Stack

**Backend:**
- Python 3.11+, FastAPI, SQLAlchemy, AsyncIO
- DroidRun + uiautomator2 (Android control)
- Puter.js (LLM API)

**Frontend:**
- React 18+, TypeScript, Vite
- TailwindCSS (with V3 Design System)
- WebSocket (real-time updates)

**Infrastructure:**
- Tailscale (VPN)
- ADB (Android Debug Bridge)
- SQLite (MVP) → PostgreSQL (production)

## 🤝 Contributing

This is a private project. For development guidelines, see [promt-dev-base.md](promt-dev-base.md).

## 📝 License

Private - All Rights Reserved

## 📧 Contact

For questions, reach out via Telegram: [Bot Token in .env]
