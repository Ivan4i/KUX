# 91_TROUBLESHOOTING_RUNBOOK.md

## Troubleshooting Runbook: Quick Solutions

### Category: Installation & Setup Issues

#### Problem: "command not found: docker"

**Symptoms:**
```bash
$ docker --version
bash: docker: command not found
```

**Solution:**
```bash
# macOS (with Homebrew)
brew install docker docker-compose

# Or download from: https://www.docker.com/products/docker-desktop

# Verify
docker --version
docker-compose --version
```

---

#### Problem: "Docker daemon not running"

**Symptoms:**
```
Cannot connect to Docker daemon at unix:///var/run/docker.sock
```

**Solution:**
```bash
# macOS
open -a Docker

# Linux
sudo systemctl start docker
sudo systemctl enable docker

# Verify
docker ps
```

---

#### Problem: "Permission denied while trying to connect to Docker daemon"

**Symptoms:**
```
Got permission denied while trying to connect to the Docker daemon socket
```

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Verify
docker ps

# Or run commands with sudo (temporary fix)
sudo docker ps
```

---

### Category: Port Conflicts

#### Problem: "Address already in use: 0.0.0.0:8000"

**Symptoms:**
```
ERROR: for backend Cannot start service backend: driver failed programming external connectivity
Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000
netstat -tulpn | grep 8000

# Kill the process
kill -9 <PID>

# Or change port in .env.local
BACKEND_PORT=8001

# Restart
./scripts/start.sh
```

**All Ports Used:**
```
5432 - PostgreSQL
6379 - Redis
8000 - Backend
5173 - Frontend
5037 - ADB
```

**Check All:**
```bash
lsof -i :5432,6379,8000,5173,5037
```

---

### Category: Database Issues

#### Problem: "connection refused - postgresql"

**Symptoms:**
```
psycopg2.OperationalError: connection refused
Is the server running on host "postgres"
```

**Solution:**
```bash
# Check if postgres container is running
docker-compose ps postgres

# View logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres

# Verify connection
docker-compose exec postgres psql -U automation_user -d multidevice_db -c "SELECT 1"
```

---

#### Problem: "database does not exist"

**Symptoms:**
```
psycopg2.ProgrammingError: database "multidevice_db" does not exist
```

**Solution:**
```bash
# Initialize database manually
docker-compose exec backend alembic upgrade head

# Or reset everything
./scripts/reset.sh
./scripts/setup.sh
```

---

#### Problem: "Alembic migration failed"

**Symptoms:**
```
FAILED: Can't find table "some_table"
```

**Solution:**
```bash
# View migration status
docker-compose exec backend alembic current

# Check history
docker-compose exec backend alembic history

# Reset migrations
docker-compose exec backend alembic downgrade base
docker-compose exec backend alembic upgrade head

# Or manually
docker-compose exec backend python -m alembic upgrade head
```

---

### Category: ADB & USB Device Issues

#### Problem: "adb: command not found"

**Symptoms:**
```bash
$ adb devices
bash: adb: command not found
```

**Solution:**
```bash
# Download Android SDK tools
# From: https://developer.android.com/studio/releases/platform-tools

# macOS
brew install android-platform-tools

# Add to PATH
export PATH=$PATH:~/Android/Sdk/platform-tools

# Verify
adb version
```

---

#### Problem: "no devices/emulators found"

**Symptoms:**
```bash
$ adb devices
List of attached devices
(no devices)

$ ./scripts/test-devices.sh
0/7 devices online
```

**Solution:**
```bash
# 1. Check USB cable connection
# 2. Enable USB debugging on device
#    Settings → Developer Options → USB Debugging → ON

# 3. Restart ADB server
adb kill-server
adb start-server

# 4. List devices again
adb devices

# 5. If still not detected, check USB permissions
lsusb  # List USB devices

# 6. Install USB rules (Linux)
sudo cp adb-config/udev-rules.txt /etc/udev/rules.d/51-android.rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# 7. Reconnect device
# Unplug USB cable and reconnect
```

---

#### Problem: "error: device unauthorized"

**Symptoms:**
```bash
$ adb devices
emulator-5554    unauthorized
```

**Solution:**
```bash
# 1. On device, check USB debugging authorization prompt
# 2. Tap "Allow" on the device

# 3. If not showing, disconnect and reconnect
adb kill-server
adb start-server
adb devices

# 4. Force authentication
adb shell exit

# 5. Or revoke all authorizations
adb kill-server
rm ~/.android/adbkey*
adb start-server
```

---

#### Problem: "Multiple ADB servers running"

**Symptoms:**
```
Multiple adb servers running - killing all
```

**Solution:**
```bash
# Kill all adb processes
pkill -f adb
killall adb

# Wait
sleep 2

# Start fresh
adb start-server

# Verify
adb devices
```

---

### Category: Redis & Caching Issues

#### Problem: "Failed to connect to redis"

**Symptoms:**
```
ConnectionRefusedError: Error 111 connecting to localhost:6379
```

**Solution:**
```bash
# Check redis status
docker-compose ps redis

# View redis logs
docker-compose logs redis

# Restart redis
docker-compose restart redis

# Verify connection
docker-compose exec redis redis-cli ping
# Should return: PONG
```

---

#### Problem: "Redis memory limit exceeded"

**Symptoms:**
```
OOM command not allowed when used memory > 'maxmemory'
```

**Solution:**
```bash
# Clear cache
docker-compose exec redis redis-cli FLUSHALL

# Or flush specific database
docker-compose exec redis redis-cli SELECT 0
docker-compose exec redis redis-cli FLUSHDB

# Increase memory limit in docker-compose.yml
# Add to redis service:
# command: redis-server --maxmemory 2gb --maxmemory-policy allkeys-lru
```

---

### Category: Celery & Task Queue Issues

#### Problem: "No workers registered"

**Symptoms:**
```
Celery worker not executing tasks
No running workers found
```

**Solution:**
```bash
# Check worker status
docker-compose ps celery-worker

# View worker logs
docker-compose logs celery-worker

# Restart worker
docker-compose restart celery-worker

# Verify worker is active
docker-compose exec celery-worker celery -A app.core.queue_manager inspect active
```

---

#### Problem: "Task stuck in queue"

**Symptoms:**
```
Task status: PENDING (forever)
Task never executes
```

**Solution:**
```bash
# List pending tasks
docker-compose exec redis redis-cli LRANGE celery 0 -1

# Clear stuck tasks
docker-compose exec redis redis-cli DEL celery

# Revoke specific task
docker-compose exec celery-worker celery -A app.core.queue_manager revoke TASK_ID

# Restart everything
./scripts/stop.sh
./scripts/start.sh
```

---

### Category: Frontend Issues

#### Problem: "CORS errors in console"

**Symptoms:**
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Solution:**
```bash
# Check CORS configuration in backend
# backend/app/main.py should have:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Verify frontend can reach backend
curl http://localhost:8000/health

# Check environment variables in .env.local
VITE_API_URL=http://localhost:8000
```

---

#### Problem: "WebSocket connection failed"

**Symptoms:**
```
WebSocket is closed before the connection is established
```

**Solution:**
```bash
# Check backend WebSocket support
# In backend/app/main.py:
from fastapi import WebSocketException
from fastapi.routing import APIRouter

# Verify frontend WebSocket URL
# In frontend/.env:
VITE_WS_URL=ws://localhost:8000

# Restart frontend
docker-compose restart frontend

# Check backend logs for WebSocket errors
docker-compose logs backend | grep -i websocket
```

---

### Category: Testing Issues

#### Problem: "pytest: command not found"

**Symptoms:**
```bash
$ pytest tests/
bash: pytest: command not found
```

**Solution:**
```bash
# Install pytest in backend container
docker-compose exec backend pip install pytest pytest-asyncio

# Or run through docker-compose
docker-compose exec backend python -m pytest tests/
```

---

#### Problem: "Tests fail with database errors"

**Symptoms:**
```
test failed: database "test_db" does not exist
```

**Solution:**
```bash
# Create test database
docker-compose exec postgres createdb -U automation_user test_db

# Run migration on test database
TEST_DATABASE_URL=postgresql://automation_user:secure_password_here@postgres:5432/test_db
docker-compose exec backend alembic upgrade head

# Or use pytest fixture to auto-create:
# conftest.py should handle test database setup
```

---

### Category: Performance Issues

#### Problem: "High memory usage / OOM killer"

**Symptoms:**
```
Killed: 9 (process killed due to memory pressure)
```

**Solution:**
```bash
# Check memory usage
docker stats

# Reduce logging level
LOG_LEVEL=WARNING

# Limit worker concurrency
docker-compose.yml celery-worker:
  command: celery -A app.core.queue_manager worker --concurrency=2

# Restart
./scripts/restart.sh
```

---

#### Problem: "Slow API responses"

**Symptoms:**
```
API endpoint takes >5 seconds
```

**Solution:**
```bash
# Check backend logs
docker-compose logs backend | grep "duration"

# Profile slow endpoints
docker-compose exec backend python -m cProfile app/main.py

# Check database query performance
EXPLAIN ANALYZE <query>

# Reduce log level for speed
LOG_LEVEL=ERROR

# Cache frequently accessed data
# Use Redis cache for Notion API calls
```

---

### Category: Integration Issues

#### Problem: "Notion API authentication failed"

**Symptoms:**
```
Invalid authorization header
Invalid API key
```

**Solution:**
```bash
# Verify API key in .env.local
NOTION_API_KEY=your_notion_key_here

# Check Notion integration setup
# In Notion:
# 1. Go to Settings & Members → Integrations
# 2. Create new integration
# 3. Copy secret key
# 4. Share database with integration

# Verify with curl
curl https://api.notion.com/v1/databases \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Notion-Version: 2022-06-28"
```

---

#### Problem: "Gemini API rate limit exceeded"

**Symptoms:**
```
429 Too Many Requests
```

**Solution:**
```bash
# Implement exponential backoff in code
# In app/services/gemini_service.py:
import time
retry_count = 0
while retry_count < 3:
    try:
        response = call_gemini_api()
        break
    except RateLimitError:
        wait_time = 2 ** retry_count
        time.sleep(wait_time)
        retry_count += 1

# Reduce request frequency
# Implement caching (already in 42_PROMPT_CACHING.md)

# Or use batch processing API
```

---

### Category: Clean Reset Procedures

#### Problem: "System state is corrupted"

**Solution - Full Reset:**
```bash
# Stop everything
./scripts/stop.sh

# Remove volumes
docker-compose down -v

# Remove containers
docker-compose rm -f

# Clean up networks
docker network prune -f

# Clear local cache
rm -rf backend/__pycache__
rm -rf frontend/node_modules/.vite

# Restart from scratch
./scripts/setup.sh
./scripts/start.sh
```

---

#### Problem: "Database needs rollback"

**Solution:**
```bash
# View migration history
docker-compose exec backend alembic history -r

# Downgrade to specific version
docker-compose exec backend alembic downgrade ae1027a6acf

# Re-upgrade
docker-compose exec backend alembic upgrade head
```

---

### Debug Mode

**Enable debug logging for all services:**

```bash
# In .env.local
LOG_LEVEL=DEBUG
DEBUG=true

# Restart
./scripts/restart.sh

# View detailed logs
./scripts/logs.sh | grep "DEBUG"
```

**Backend Debug Console:**

```bash
# SSH into backend container
docker-compose exec backend bash

# Run Python REPL
python

# Test imports
>>> from app.models.device import Device
>>> from app.services.adb_service import ADBService
>>> adb = ADBService()
>>> print(adb.get_devices())
```

---

### Emergency Commands

```bash
# Kill all Docker containers
docker kill $(docker ps -q)

# Remove all Docker containers
docker rm $(docker ps -aq)

# Full Docker cleanup
docker system prune -a

# Check disk space
df -h

# Monitor system
top
htop  # if installed

# Check network connections
netstat -tulpn

# Force port kill
lsof -ti:8000 | xargs kill -9
```

---

### Getting Help

**If problem persists:**

1. **Collect diagnostic info:**
```bash
./scripts/logs.sh > debug_logs.txt
docker-compose ps > services.txt
docker stats > resources.txt
adb devices > devices.txt
```

2. **Check documentation:**
- 90_DEPLOYMENT_GUIDE.md - Setup issues
- 80_BACKEND_ARCHITECTURE.md - Backend architecture
- 70_FRONTEND_ARCHITECTURE.md - Frontend issues
- Individual component files (README sections)

3. **Review error message:**
- Search error message in this runbook
- Check component-specific documentation
- Review logs for root cause

4. **Reset and retry:**
```bash
./scripts/reset.sh
./scripts/setup.sh
./scripts/start.sh
```

---

## End of 91_TROUBLESHOOTING_RUNBOOK.md