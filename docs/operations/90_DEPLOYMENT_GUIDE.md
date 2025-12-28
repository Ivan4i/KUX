# 90_DEPLOYMENT_GUIDE.md

## Local Deployment Guide: One Command Setup

### Philosophy

```
✅ NO HACKS. NO WORKAROUNDS.
✅ EVERYTHING RUNS LOCALLY
✅ PERSISTENT USB CONNECTIONS (ADB over USB)
✅ ONE COMMAND TO START
✅ FAST TEARDOWN & RESET
✅ CLEAN TESTING EVERY TIME
```

### Prerequisites

```bash
# Required versions
- Docker Desktop 4.20+
- Docker Compose 2.20+
- Python 3.11+
- Node 18+
- Android SDK tools (ADB)
- USB Hub (for 7 devices)

# Verify setup
docker --version          # Docker version 20.10+
docker-compose --version  # Docker Compose 2.20+
python --version          # Python 3.11+
node --version            # Node 18+
adb version               # ADB version 34+
```

### Project Structure

```
multidevice-automation/
├── docker-compose.yml              # Main orchestration
├── docker-compose.override.yml     # Local development overrides
├── .env.local                      # Local environment variables
├── .env.example                    # Template
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   ├── migrations/
│   └── main.py
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│
├── adb-config/
│   ├── adb-connections.sh         # USB ADB setup script
│   ├── devices.json               # Device registry
│   └── udev-rules.txt             # USB permissions
│
├── scripts/
│   ├── setup.sh                   # One-time setup
│   ├── start.sh                   # Start all services
│   ├── stop.sh                    # Stop all services
│   ├── reset.sh                   # Clean state
│   ├── test-devices.sh            # Verify USB connections
│   └── logs.sh                    # View live logs
│
└── tests/
    ├── integration/
    ├── e2e/
    └── README.md
```

### 1. Initial Setup (ONE TIME)

```bash
# Clone repository
git clone https://github.com/your-org/multidevice-automation.git
cd multidevice-automation

# Run setup (installs everything)
chmod +x scripts/setup.sh
./scripts/setup.sh

# Expected output:
# ✅ Docker environment ready
# ✅ Environment variables configured
# ✅ USB device drivers installed
# ✅ Databases initialized
# ✅ Ready to start!
```

### setup.sh - Detailed

```bash
#!/bin/bash
# scripts/setup.sh

set -e  # Exit on error

echo "🔧 MultiDevice Automation - Initial Setup"
echo "=========================================="

# 1. Check dependencies
echo "📋 Checking dependencies..."

check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 not found. Install it first."
        exit 1
    fi
    echo "✅ $1 found"
}

check_command docker
check_command docker-compose
check_command python3
check_command node
check_command adb

# 2. Setup environment
echo ""
echo "⚙️  Setting up environment..."

if [ ! -f .env.local ]; then
    cp .env.example .env.local
    echo "✅ Created .env.local (edit with your settings)"
else
    echo "✅ .env.local already exists"
fi

# 3. Install USB rules
echo ""
echo "🔌 Installing USB udev rules..."

if [ -f adb-config/udev-rules.txt ]; then
    sudo cp adb-config/udev-rules.txt /etc/udev/rules.d/51-android.rules
    sudo udevadm control --reload-rules
    sudo udevadm trigger
    echo "✅ USB permissions configured"
else
    echo "⚠️  USB rules file not found"
fi

# 4. Build Docker images
echo ""
echo "🐳 Building Docker images..."

docker-compose build

echo "✅ Images built"

# 5. Start services
echo ""
echo "🚀 Starting services..."

docker-compose up -d

sleep 5

# 6. Initialize databases
echo ""
echo "📦 Initializing databases..."

docker-compose exec -T backend alembic upgrade head

echo "✅ Databases initialized"

# 7. Health check
echo ""
echo "🏥 Running health check..."

MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Backend healthy"
        break
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 1
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "❌ Backend failed to start"
    exit 1
fi

# 8. Detect USB devices
echo ""
echo "🔍 Detecting USB Android devices..."

chmod +x adb-config/adb-connections.sh
./adb-config/adb-connections.sh

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Connect 7 Android devices via USB"
echo "  2. Run: ./scripts/start.sh"
echo "  3. Open: http://localhost:5173"
echo ""
```

### 2. Start System

```bash
# Start everything
./scripts/start.sh

# Expected output:
# 🚀 Starting Docker services...
# ✅ PostgreSQL running (5432)
# ✅ Redis running (6379)
# ✅ Backend running (8000)
# ✅ Frontend running (5173)
# ✅ Celery workers ready
# 
# Access:
#   Frontend: http://localhost:5173
#   Backend:  http://localhost:8000
#   API Docs: http://localhost:8000/docs
```

### start.sh - Implementation

```bash
#!/bin/bash
# scripts/start.sh

set -e

echo "🚀 Starting MultiDevice Automation"

# Start containers
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be ready..."

# Check backend
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Backend ready"
        break
    fi
    sleep 1
done

# Check frontend
for i in {1..30}; do
    if curl -s http://localhost:5173 > /dev/null; then
        echo "✅ Frontend ready"
        break
    fi
    sleep 1
done

# List services
echo ""
echo "📊 Running services:"
docker-compose ps

echo ""
echo "✅ All services started!"
echo ""
echo "Access points:"
echo "  🖥️  Dashboard:  http://localhost:5173"
echo "  📚 API Docs:   http://localhost:8000/docs"
echo "  ⚙️  Swagger UI: http://localhost:8000/redoc"
echo ""
echo "Commands:"
echo "  View logs:    ./scripts/logs.sh"
echo "  Stop system:  ./scripts/stop.sh"
echo "  Reset state:  ./scripts/reset.sh"
echo ""
```

### 3. Environment Variables (.env.local)

```env
# .env.local

# ===== DOCKER =====
COMPOSE_PROJECT_NAME=multidevice
DOCKER_BUILDKIT=1

# ===== DATABASE =====
POSTGRES_USER=automation_user
POSTGRES_PASSWORD=secure_password_here
POSTGRES_DB=multidevice_db
DATABASE_URL=postgresql://automation_user:secure_password_here@postgres:5432/multidevice_db

# ===== REDIS =====
REDIS_URL=redis://redis:6379/0
REDIS_CACHE_DB=1

# ===== CELERY =====
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/1

# ===== API KEYS =====
GEMINI_API_KEY=your_gemini_key_here
NOTION_API_KEY=your_notion_key_here
ALIGNUI_API_KEY=your_alignui_key_here

# ===== BACKEND =====
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
SECRET_KEY=your_secret_key_here
DEBUG=false
LOG_LEVEL=INFO

# ===== FRONTEND =====
FRONTEND_HOST=localhost
FRONTEND_PORT=5173
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# ===== ADB =====
ADB_PORT=5037
ADB_HOST=localhost
MAX_DEVICES=7

# ===== TESTING =====
TESTING_MODE=true
SKIP_DEVICE_VALIDATION=false
```

### Docker Compose Setup

```yaml
# docker-compose.yml

version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: multidevice-db
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - automation

  # Redis Cache & Queue
  redis:
    image: redis:7-alpine
    container_name: multidevice-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - automation

  # FastAPI Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: multidevice-backend
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
      CELERY_BROKER: ${CELERY_BROKER}
      CELERY_BACKEND: ${CELERY_BACKEND}
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      NOTION_API_KEY: ${NOTION_API_KEY}
      ALIGNUI_API_KEY: ${ALIGNUI_API_KEY}
      SECRET_KEY: ${SECRET_KEY}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: >
      sh -c "
        alembic upgrade head &&
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
      "
    networks:
      - automation

  # Celery Worker
  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: multidevice-celery
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
      CELERY_BROKER: ${CELERY_BROKER}
      CELERY_BACKEND: ${CELERY_BACKEND}
    depends_on:
      redis:
        condition: service_healthy
      postgres:
        condition: service_healthy
    command: celery -A app.core.queue_manager.celery_app worker --loglevel=info --concurrency=4
    networks:
      - automation

  # React Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: multidevice-frontend
    environment:
      VITE_API_URL: http://backend:8000
      VITE_WS_URL: ws://backend:8000
    ports:
      - "5173:5173"
    depends_on:
      - backend
    volumes:
      - ./frontend/src:/app/src
    command: npm run dev
    networks:
      - automation

volumes:
  postgres_data:
  redis_data:

networks:
  automation:
    driver: bridge
```

### 4. Device Testing

```bash
# Test USB connections
./scripts/test-devices.sh

# Expected output:
# 🔍 Scanning USB devices...
# ✅ Device 1: emulator-5554 (Online)
# ✅ Device 2: 192.168.1.100:5555 (Online)
# ✅ Device 3: device123 (Online)
# ✅ Device 4: device456 (Online)
# ✅ Device 5: device789 (Online)
# ✅ Device 6: deviceABC (Online)
# ✅ Device 7: deviceDEF (Online)
# 
# 7/7 devices online
```

### 5. Running Tests

```bash
# Integration tests
docker-compose exec backend pytest tests/integration -v

# E2E tests
docker-compose exec backend pytest tests/e2e -v

# Coverage report
docker-compose exec backend pytest --cov=app tests/

# All tests
./scripts/run-tests.sh
```

### 6. Viewing Logs

```bash
# All services
./scripts/logs.sh

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery-worker
docker-compose logs -f frontend

# Real-time JSON logs
docker-compose logs --timestamps backend
```

### 7. Stop & Cleanup

```bash
# Stop services (keep data)
./scripts/stop.sh

# Full reset (cleans everything)
./scripts/reset.sh

# Remove specific service
docker-compose down postgres
```

### 8. Development Workflow

```bash
# 1. Start everything
./scripts/start.sh

# 2. Make code changes (hot reload enabled)
# - Edit backend code → auto-reload
# - Edit frontend code → auto-rebuild

# 3. Access dashboard
open http://localhost:5173

# 4. Test API
curl http://localhost:8000/health

# 5. View logs
./scripts/logs.sh

# 6. Stop when done
./scripts/stop.sh
```

### USB ADB Setup (for 7 devices)

```bash
#!/bin/bash
# adb-config/adb-connections.sh

echo "🔌 Setting up USB ADB connections..."

# Kill existing adb server
adb kill-server

# Start adb server
adb start-server

# Wait for server to start
sleep 2

# List devices
echo "📱 Connected devices:"
adb devices

# Count devices
DEVICE_COUNT=$(adb devices | grep -c "device$")

if [ $DEVICE_COUNT -lt 7 ]; then
    echo "⚠️  Only $DEVICE_COUNT/7 devices connected"
    echo "Please check USB connections"
else
    echo "✅ All 7 devices connected"
fi

# Save device list
adb devices -l > adb-config/devices.json

echo "✅ USB connections ready"
```

### Quick Reference

```
┌─────────────────────────────────────┐
│    MULTIDEVICE QUICK COMMANDS       │
├─────────────────────────────────────┤
│ ./scripts/setup.sh        Setup     │
│ ./scripts/start.sh        Start     │
│ ./scripts/stop.sh         Stop      │
│ ./scripts/reset.sh        Reset     │
│ ./scripts/test-devices.sh Verify    │
│ ./scripts/logs.sh         Monitor   │
│ ./scripts/run-tests.sh    Test      │
└─────────────────────────────────────┘
```

### Troubleshooting During Deployment

```
❌ "Port already in use"
   → lsof -i :8000
   → kill -9 <PID>

❌ "ADB not found"
   → export PATH=$PATH:~/Android/Sdk/platform-tools

❌ "USB device not detected"
   → Check USB cable connection
   → Run: adb kill-server && adb start-server
   → Check: adb devices

❌ "Docker network error"
   → docker network prune
   → docker-compose down
   → docker-compose up

❌ "Database connection failed"
   → docker-compose logs postgres
   → Ensure DATABASE_URL is correct in .env.local

See 91_TROUBLESHOOTING_RUNBOOK.md for detailed solutions
```

---

## End of 90_DEPLOYMENT_GUIDE.md