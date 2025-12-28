"""Pydantic schemas for API request/response validation"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


# Enums for type safety
class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "Pending"
    RUNNING = "Running"
    SENT = "Sent"
    FAILED = "Failed"


class DeviceStatusEnum(str, Enum):
    """Device status enumeration"""
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    SLEEPING = "sleeping"
    OVERHEATING = "overheating"
    LOW_BATTERY = "low_battery"
    ERROR = "error"


class LogStatus(str, Enum):
    """Log status enumeration"""
    SUCCESS = "success"
    WARNING = "warning"
    FAILED = "failed"
    INFO = "info"


# Device Schemas
class DeviceBase(BaseModel):
    """Base device schema"""
    id: str
    name: str
    location: Optional[str] = None
    timezone: Optional[str] = None


class DeviceStatus(BaseModel):
    """Device status response with validation"""
    id: str = Field(..., min_length=1, max_length=100, description="Unique device identifier")
    name: str = Field(..., min_length=1, max_length=200, description="Device display name")
    current_status: DeviceStatusEnum = Field(..., description="Current device status")
    battery_level: int = Field(..., ge=0, le=100, description="Battery percentage (0-100)")
    temperature: float = Field(..., ge=-20.0, le=80.0, description="Device temperature in Celsius")
    memory_usage: int = Field(..., ge=0, le=100, description="Memory usage percentage (0-100)")
    active_tasks: int = Field(default=0, ge=0, le=10, description="Number of active tasks (max 10)")
    last_heartbeat: Optional[datetime] = Field(None, description="Last successful device ping")

    class Config:
        from_attributes = True


class DeviceCreate(DeviceBase):
    """Create device request"""
    device_id: str


# Task Schemas
class TaskBase(BaseModel):
    """Base task schema"""
    task_type: str
    content: Dict[str, Any]


class TaskCreate(TaskBase):
    """Create task request"""
    notion_id: Optional[str] = None
    device_id: Optional[str] = None


class TaskResponse(BaseModel):
    """Task response with validation"""
    id: str = Field(..., description="Unique task identifier")
    task_type: str = Field(..., min_length=1, max_length=50, description="Type of task (whatsapp, linkedin, etc)")
    status: TaskStatus = Field(..., description="Current task status")
    device_id: Optional[str] = Field(None, description="Assigned device ID")
    content: Dict[str, Any] = Field(..., description="Task content and parameters")
    created_at: datetime = Field(..., description="Task creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Task start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Task completion timestamp")
    attempt_count: int = Field(default=0, ge=0, le=10, description="Number of execution attempts (max 10)")
    error_message: Optional[str] = Field(None, max_length=2000, description="Last error message")

    class Config:
        from_attributes = True


# Log Schemas
class LogBase(BaseModel):
    """Base log schema"""
    action: str
    status: str
    device_id: Optional[str] = None
    task_id: Optional[str] = None


class LogCreate(LogBase):
    """Create log request"""
    duration_seconds: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class LogResponse(BaseModel):
    """Log response with validation"""
    id: int = Field(..., gt=0, description="Unique log entry ID")
    timestamp: datetime = Field(..., description="Log entry timestamp")
    device_id: Optional[str] = Field(None, max_length=100, description="Device that performed action")
    task_id: Optional[str] = Field(None, description="Associated task ID")
    action: str = Field(..., min_length=1, max_length=100, description="Action type performed")
    status: LogStatus = Field(..., description="Action result status")
    duration_seconds: Optional[float] = Field(None, ge=0.0, le=3600.0, description="Action duration (max 1 hour)")
    error_message: Optional[str] = Field(None, max_length=2000, description="Error details if failed")
    screenshot_path: Optional[str] = Field(None, max_length=500, description="Path to screenshot if captured")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional action metadata")

    class Config:
        from_attributes = True


# Health Check
class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime


# Query Parameter Schemas
class TaskQueryParams(BaseModel):
    """Query parameters for task listing with validation"""
    status: Optional[str] = Field(None, max_length=20, description="Filter by task status")
    device_id: Optional[str] = Field(None, max_length=100, description="Filter by device ID")
    limit: int = Field(default=50, ge=1, le=1000, description="Maximum number of results (1-1000)")
    offset: int = Field(default=0, ge=0, description="Number of results to skip")


class LogQueryParams(BaseModel):
    """Query parameters for log listing with validation"""
    device_id: Optional[str] = Field(None, max_length=100, description="Filter by device ID")
    task_id: Optional[str] = Field(None, description="Filter by task ID")
    status: Optional[str] = Field(None, max_length=20, description="Filter by log status")
    action_type: Optional[str] = Field(None, max_length=100, description="Filter by action type")
    hours: int = Field(default=24, ge=1, le=720, description="Time range in hours (1-720/30 days)")
    limit: int = Field(default=100, ge=1, le=10000, description="Maximum number of results (1-10000)")


class NotionSyncParams(BaseModel):
    """Parameters for Notion sync with validation"""
    limit: int = Field(default=10, ge=1, le=100, description="Max tasks to sync (1-100)")


# ============================================
# SCENARIO SCHEMAS
# ============================================

class ScenarioStatusEnum(str, Enum):
    """Scenario status enumeration"""
    DRAFT = "draft"
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatusEnum(str, Enum):
    """Step status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class AgentTypeEnum(str, Enum):
    """Available agent types"""
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TELEGRAM = "telegram"
    YOUTUBE = "youtube"
    SMS = "sms"
    NOTION = "notion"
    SCRAPER = "scraper"


# Step Schemas
class ScenarioStepBase(BaseModel):
    """Base schema for scenario step"""
    name: str = Field(..., min_length=1, max_length=200, description="Step name")
    agent_type: AgentTypeEnum = Field(..., description="Agent type for this step")
    action: str = Field(..., min_length=1, max_length=100, description="Action to perform")
    order: int = Field(..., ge=1, le=100, description="Execution order (1-100)")
    config: Optional[Dict[str, Any]] = Field(None, description="Step-specific configuration")
    prompt_template_id: Optional[str] = Field(None, description="Prompt template ID")
    delay_before_seconds: int = Field(default=0, ge=0, le=3600, description="Delay before step (seconds)")
    timeout_seconds: int = Field(default=300, ge=10, le=3600, description="Step timeout (seconds)")
    max_attempts: int = Field(default=3, ge=1, le=10, description="Max retry attempts")
    condition: Optional[Dict[str, Any]] = Field(None, description="Execution condition")
    skip_on_failure: bool = Field(default=False, description="Skip this step if previous failed")


class ScenarioStepCreate(ScenarioStepBase):
    """Schema for creating a scenario step"""
    pass


class ScenarioStepUpdate(BaseModel):
    """Schema for updating a scenario step"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    agent_type: Optional[AgentTypeEnum] = None
    action: Optional[str] = Field(None, min_length=1, max_length=100)
    order: Optional[int] = Field(None, ge=1, le=100)
    config: Optional[Dict[str, Any]] = None
    prompt_template_id: Optional[str] = None
    delay_before_seconds: Optional[int] = Field(None, ge=0, le=3600)
    timeout_seconds: Optional[int] = Field(None, ge=10, le=3600)
    max_attempts: Optional[int] = Field(None, ge=1, le=10)
    condition: Optional[Dict[str, Any]] = None
    skip_on_failure: Optional[bool] = None


class ScenarioStepResponse(ScenarioStepBase):
    """Response schema for scenario step"""
    id: str
    scenario_id: str
    status: StepStatusEnum = Field(default=StepStatusEnum.PENDING)
    attempt_count: int = Field(default=0)
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


# Scenario Schemas
class ScenarioBase(BaseModel):
    """Base schema for scenario"""
    name: str = Field(..., min_length=1, max_length=200, description="Scenario name")
    description: Optional[str] = Field(None, max_length=2000, description="Scenario description")
    device_id: Optional[str] = Field(None, description="Assigned device ID")
    priority: int = Field(default=5, ge=1, le=10, description="Priority (1-10, higher=more important)")

    # Scheduling
    cron_expression: Optional[str] = Field(None, max_length=100, description="CRON expression for scheduling")
    scheduled_at: Optional[datetime] = Field(None, description="One-time scheduled execution")
    repeat_count: int = Field(default=0, ge=0, description="Number of repeats (0=unlimited)")

    # Interval settings
    min_interval_seconds: int = Field(default=300, ge=30, le=86400, description="Min interval between actions")
    max_interval_seconds: int = Field(default=600, ge=60, le=86400, description="Max interval between actions")

    # Notion integration
    notion_campaign_id: Optional[str] = Field(None, description="Notion campaign ID")

    # Extra config
    config: Optional[Dict[str, Any]] = Field(None, description="Additional configuration")


class ScenarioCreate(ScenarioBase):
    """Schema for creating a scenario"""
    steps: Optional[list[ScenarioStepCreate]] = Field(None, description="Scenario steps")


class ScenarioUpdate(BaseModel):
    """Schema for updating a scenario"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    device_id: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=10)
    cron_expression: Optional[str] = Field(None, max_length=100)
    scheduled_at: Optional[datetime] = None
    repeat_count: Optional[int] = Field(None, ge=0)
    min_interval_seconds: Optional[int] = Field(None, ge=30, le=86400)
    max_interval_seconds: Optional[int] = Field(None, ge=60, le=86400)
    notion_campaign_id: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class ScenarioResponse(ScenarioBase):
    """Response schema for scenario"""
    id: str
    status: ScenarioStatusEnum = Field(default=ScenarioStatusEnum.DRAFT)
    current_step_index: int = Field(default=0)
    total_steps: int = Field(default=0)
    current_repeat: int = Field(default=0)

    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None

    success_count: int = Field(default=0)
    failure_count: int = Field(default=0)
    error_message: Optional[str] = None

    steps: list[ScenarioStepResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class ScenarioListResponse(BaseModel):
    """Response schema for scenario list (without steps)"""
    id: str
    name: str
    description: Optional[str] = None
    status: ScenarioStatusEnum
    device_id: Optional[str] = None
    priority: int
    total_steps: int
    current_step_index: int
    created_at: datetime
    updated_at: datetime
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    success_count: int
    failure_count: int

    class Config:
        from_attributes = True


# Scenario execution requests
class ScenarioRunRequest(BaseModel):
    """Request to run a scenario"""
    device_id: Optional[str] = Field(None, description="Override device ID")
    skip_to_step: Optional[int] = Field(None, ge=1, description="Skip to specific step")
    dry_run: bool = Field(default=False, description="Test mode (no actual execution)")


class ScenarioActionRequest(BaseModel):
    """Request for scenario actions (pause, resume, cancel)"""
    action: str = Field(..., description="Action: pause, resume, cancel, restart")


# Queue/Scheduler schemas
class QueuedTaskResponse(BaseModel):
    """Response for queued task"""
    id: str
    type: str  # scenario or task
    reference_id: str
    priority: int
    status: str
    queued_at: datetime
    started_at: Optional[datetime] = None
    estimated_wait_seconds: Optional[int] = None


class SchedulerStatusResponse(BaseModel):
    """Response for scheduler status"""
    is_running: bool
    active_jobs: int
    queued_jobs: int
    completed_today: int
    failed_today: int
    next_scheduled_job: Optional[Dict[str, Any]] = None
