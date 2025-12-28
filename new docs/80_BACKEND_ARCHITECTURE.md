# 80_BACKEND_ARCHITECTURE.md

## Backend Architecture: FastAPI & Core Services

### Tech Stack

```
Backend Stack:
┌─────────────────────────────────────┐
│  Framework: FastAPI                 │
│  Async: asyncio + aiohttp           │
│  Queue: Celery + Redis              │
│  Database: PostgreSQL + SQLAlchemy  │
│  WebSocket: Socket.IO               │
│  Caching: Redis                     │
│  Deployment: Docker + Gunicorn      │
└─────────────────────────────────────┘

Why FastAPI?
✅ Async/await native (handles concurrency)
✅ Type hints (automatic validation)
✅ Auto API documentation (Swagger)
✅ High performance (benchmarks beat Flask)
✅ WebSocket support built-in
✅ Easy to test
```

### Project Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration (env vars)
│   ├── dependencies.py            # Dependency injection
│   │
│   ├── api/
│   │   ├── v1/
│   │   │   ├── devices.py         # Device endpoints
│   │   │   ├── workflows.py       # Workflow endpoints
│   │   │   ├── tasks.py           # Task endpoints
│   │   │   ├── analytics.py       # Analytics endpoints
│   │   │   └── auth.py            # Authentication
│   │
│   ├── models/
│   │   ├── device.py              # Device DB model
│   │   ├── workflow.py            # Workflow DB model
│   │   ├── task.py                # Task DB model
│   │   └── user.py                # User model
│   │
│   ├── schemas/
│   │   ├── device.py              # Device Pydantic schema
│   │   ├── workflow.py            # Workflow schema
│   │   ├── task.py                # Task schema
│   │   └── response.py            # Response schemas
│   │
│   ├── services/
│   │   ├── device_service.py      # Device business logic
│   │   ├── workflow_service.py    # Workflow execution
│   │   ├── task_service.py        # Task management
│   │   ├── adb_service.py         # ADB wrapper
│   │   └── notification_service.py# WebSocket notifications
│   │
│   ├── core/
│   │   ├── execution_engine.py    # Workflow execution
│   │   ├── scheduler.py           # Task scheduler
│   │   ├── queue_manager.py       # Job queue (Celery)
│   │   └── error_handler.py       # Error handling
│   │
│   └── utils/
│       ├── logger.py              # Logging setup
│       ├── decorators.py          # Custom decorators
│       └── helpers.py             # Utility functions
│
├── migrations/                     # Alembic migrations
├── tests/
│   ├── test_devices.py
│   ├── test_workflows.py
│   └── test_tasks.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── main.py
```

### Main FastAPI Application

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1 import devices, workflows, tasks, analytics
from app.core.scheduler import TaskScheduler
from app.core.queue_manager import QueueManager

# Initialize services
scheduler = TaskScheduler()
queue_manager = QueueManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("🚀 Starting backend services...")
    
    # Start scheduler
    await scheduler.start()
    
    # Start queue manager
    await queue_manager.start()
    
    yield
    
    print("🛑 Shutting down services...")
    await scheduler.stop()
    await queue_manager.stop()

# Create FastAPI app
app = FastAPI(
    title="MultiDevice Automation API",
    description="Control multiple Android devices with Gemini AI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    devices.router,
    prefix="/api/v1/devices",
    tags=["devices"]
)

app.include_router(
    workflows.router,
    prefix="/api/v1/workflows",
    tags=["workflows"]
)

app.include_router(
    tasks.router,
    prefix="/api/v1/tasks",
    tags=["tasks"]
)

app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["analytics"]
)

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "scheduler": scheduler.is_running,
            "queue": queue_manager.is_running,
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### Device Endpoints

```python
# app/api/v1/devices.py
from fastapi import APIRouter, HTTPException, WebSocket
from app.schemas.device import DeviceResponse, DeviceUpdate
from app.services.device_service import DeviceService
from typing import List

router = APIRouter()
device_service = DeviceService()

@router.get("/", response_model=List[DeviceResponse])
async def list_devices():
    """Get all connected devices"""
    devices = await device_service.get_all_devices()
    return devices

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str):
    """Get specific device info"""
    device = await device_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: str, update: DeviceUpdate):
    """Update device settings"""
    device = await device_service.update_device(device_id, update)
    return device

@router.post("/{device_id}/click")
async def click_device(device_id: str, x: int, y: int):
    """Click on device screen"""
    result = await device_service.click(device_id, x, y)
    return {"success": result}

@router.post("/{device_id}/type")
async def type_on_device(device_id: str, text: str):
    """Type text on device"""
    result = await device_service.type_text(device_id, text)
    return {"success": result}

@router.get("/{device_id}/screenshot")
async def screenshot(device_id: str):
    """Get device screenshot"""
    path = await device_service.take_screenshot(device_id)
    return {"path": path}

@router.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    """WebSocket for real-time device updates"""
    await websocket.accept()
    
    try:
        # Send initial device state
        device = await device_service.get_device(device_id)
        await websocket.send_json(device.dict())
        
        # Stream updates
        async for update in device_service.stream_device_updates(device_id):
            await websocket.send_json(update)
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    
    finally:
        await websocket.close()
```

### Workflow Endpoints

```python
# app/api/v1/workflows.py
from fastapi import APIRouter, HTTPException
from app.schemas.workflow import WorkflowCreate, WorkflowResponse
from app.services.workflow_service import WorkflowService
from typing import List

router = APIRouter()
workflow_service = WorkflowService()

@router.get("/", response_model=List[WorkflowResponse])
async def list_workflows():
    """Get all workflows"""
    workflows = await workflow_service.get_all_workflows()
    return workflows

@router.post("/", response_model=WorkflowResponse)
async def create_workflow(workflow: WorkflowCreate):
    """Create new workflow"""
    new_workflow = await workflow_service.create_workflow(workflow)
    return new_workflow

@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str):
    """Get workflow details"""
    workflow = await workflow_service.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(workflow_id: str, workflow: WorkflowCreate):
    """Update workflow"""
    updated = await workflow_service.update_workflow(workflow_id, workflow)
    return updated

@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Delete workflow"""
    await workflow_service.delete_workflow(workflow_id)
    return {"success": True}

@router.post("/{workflow_id}/execute")
async def execute_workflow(workflow_id: str, device_id: str):
    """Execute workflow on device"""
    task_id = await workflow_service.execute(workflow_id, device_id)
    return {"task_id": task_id}

@router.get("/{workflow_id}/stats")
async def workflow_stats(workflow_id: str):
    """Get workflow execution stats"""
    stats = await workflow_service.get_stats(workflow_id)
    return stats
```

### Database Configuration

```python
# app/config.py
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/multidevice_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Celery
    CELERY_BROKER: str = "redis://localhost:6379/0"
    CELERY_BACKEND: str = "redis://localhost:6379/0"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()

# SQLAlchemy setup
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=40,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

async def get_db():
    """Dependency: Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Requirements

```
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.4
aiohttp==3.9.1
python-socketio==5.10.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app
COPY main.py .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: multidevice_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Redis (for caching & queue)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # FastAPI Backend
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/multidevice_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - .:/app

  # Celery Worker
  celery:
    build: .
    command: celery -A app.core.queue_manager.celery_app worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/multidevice_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
```

---

## End of 80_BACKEND_ARCHITECTURE.md