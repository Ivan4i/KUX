"""API Routes package"""

from .devices import router as devices_router
from .tasks import router as tasks_router
from .logs import router as logs_router
from .scenarios import router as scenarios_router
from .settings import router as settings_router
from .workflows import router as workflows_router

__all__ = [
    "devices_router",
    "tasks_router",
    "logs_router",
    "scenarios_router",
    "settings_router",
    "workflows_router",
]
