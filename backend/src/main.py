"""Main FastAPI Application - Android Agent Platform Backend"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from .database.db import engine, Base, get_db
from .device_manager.manager import device_manager
from .routes import devices_router, tasks_router, logs_router, scenarios_router, settings_router
from .websocket import websocket_router
from .websocket.manager import ws_manager
from .config import get_settings
from .middleware import setup_error_handlers

# Orchestration imports
from .orchestration.queue_manager import queue_manager
from .orchestration.task_scheduler import task_scheduler
from .orchestration.scenario_runner import scenario_runner

# Agent imports (register available agents)
from .agents.whatsapp_agent import whatsapp_agent


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events: startup and shutdown

    Startup:
    - Initialize database
    - Connect to devices
    - Start health monitoring

    Shutdown:
    - Disconnect from devices
    - Close database connections
    """
    # Startup
    logger.info("🚀 Starting Android Agent Platform Backend...")

    try:
        # Create database tables
        logger.info("📊 Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.success("✅ Database initialized")

        # Initialize Device Manager (loads config, connects devices, starts monitoring)
        logger.info("📱 Initializing Device Manager...")
        await device_manager.initialize()
        logger.success("✅ Device Manager initialized")

        # Initialize Orchestration System
        logger.info("⚙️ Initializing Orchestration System...")

        # Connect WebSocket manager to orchestration components
        queue_manager.set_websocket_manager(ws_manager)
        task_scheduler.set_websocket_manager(ws_manager)
        task_scheduler.set_queue_manager(queue_manager)
        task_scheduler.set_db_factory(get_db)
        scenario_runner.set_websocket_manager(ws_manager)
        scenario_runner.set_db_factory(get_db)
        scenario_runner.set_device_manager(device_manager)

        # Register available agents
        scenario_runner.register_agent("whatsapp", whatsapp_agent)
        # TODO: Register other agents as they are implemented
        # scenario_runner.register_agent("instagram", instagram_agent)
        # scenario_runner.register_agent("linkedin", linkedin_agent)

        # Start Queue Manager
        logger.info("📋 Starting Queue Manager...")
        await queue_manager.start()
        logger.success("✅ Queue Manager started")

        # Start Task Scheduler
        logger.info("⏰ Starting Task Scheduler...")
        await task_scheduler.start()
        await task_scheduler.load_from_database()
        logger.success("✅ Task Scheduler started")

        logger.success("🎉 Backend startup complete!")

    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise

    yield  # Application is running

    # Shutdown
    logger.info("🛑 Shutting down Android Agent Platform Backend...")

    try:
        # Stop Task Scheduler
        logger.info("⏰ Stopping Task Scheduler...")
        await task_scheduler.stop()
        logger.success("✅ Task Scheduler stopped")

        # Stop Queue Manager
        logger.info("📋 Stopping Queue Manager...")
        await queue_manager.stop()
        logger.success("✅ Queue Manager stopped")

        # Shutdown Device Manager (stops monitoring, disconnects devices)
        logger.info("📱 Shutting down Device Manager...")
        await device_manager.shutdown()
        logger.success("✅ Device Manager shut down")

        logger.success("👋 Backend shutdown complete")

    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")


# Create FastAPI app
settings = get_settings()

app = FastAPI(
    title="Android Agent Platform API",
    description="Backend API for Android automation platform (WhatsApp, LinkedIn, Instagram)",
    version="1.0.0",
    lifespan=lifespan
)

# Setup global error handlers
setup_error_handlers(app)

# CORS middleware (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(devices_router)
app.include_router(tasks_router)
app.include_router(logs_router)
app.include_router(scenarios_router)
app.include_router(settings_router)
app.include_router(websocket_router)


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint

    Returns:
        dict: Health status
    """
    return {
        "status": "ok",
        "service": "Android Agent Platform",
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint

    Returns:
        dict: Welcome message
    """
    return {
        "message": "Android Agent Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


# Startup message
@app.on_event("startup")
async def startup_message():
    """Print startup message"""
    logger.info("=" * 60)
    logger.info("🤖 Android Agent Platform Backend")
    logger.info("=" * 60)
    logger.info(f"📝 Docs: http://localhost:8000/docs")
    logger.info(f"🏥 Health: http://localhost:8000/api/health")
    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Development mode
        log_level="info"
    )
