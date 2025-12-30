"""ORM models for database tables"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid


from .db import Base


# Enums for database
class ScenarioStatus(str, enum.Enum):
    """Scenario execution status"""
    DRAFT = "draft"
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(str, enum.Enum):
    """Scenario step execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class AgentType(str, enum.Enum):
    """Available agent types"""
    WHATSAPP = "whatsapp"
    MAX = "max"
    SMS = "sms"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TELEGRAM = "telegram"
    NOTION = "notion"
    SCRAPER = "scraper"


class TaskStatus(str, enum.Enum):
    """Task execution status"""
    PENDING = "pending"
    PROCESSING = "processing"
    SENT = "sent"
    FAILED = "failed"
    CONFIRMED = "confirmed"


class DeviceStatus(str, enum.Enum):
    """Device status"""
    OK = "ok"
    SLOW = "slow"
    OFFLINE = "offline"
    MAINTENANCE_NEEDED = "maintenance_needed"


class Device(Base):
    """Device model - represents a Google Pixel device"""
    __tablename__ = "devices"

    id = Column(String, primary_key=True)  # e.g., "pixel-th-1"
    name = Column(String, nullable=False)  # e.g., "Pixel-TH-1"
    device_id = Column(String, unique=True)  # ADB device ID
    location = Column(String)  # e.g., "Bangkok, Thailand"
    timezone = Column(String)  # e.g., "Asia/Bangkok"
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    current_status = Column(String, default="offline")  # online, offline, sleeping
    battery_level = Column(Integer, default=0)  # 0-100
    temperature = Column(Float, default=0.0)  # Celsius
    memory_usage = Column(Integer, default=0)  # Percentage
    active_tasks = Column(Integer, default=0)

    # Relationship
    tasks = relationship("Task", back_populates="device")
    logs = relationship("Log", back_populates="device")


class Task(Base):
    """Task model - represents a WhatsApp message to send"""
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    notion_id = Column(String, unique=True, nullable=True)  # Notion page ID
    task_type = Column(String, nullable=False)  # 'whatsapp', 'linkedin', 'instagram'
    status = Column(String, default="pending")  # pending, running, success, failed
    device_id = Column(String, ForeignKey('devices.id'), nullable=True)

    # Notion-specific fields
    priority = Column(Integer, default=0)  # 0-5
    scheduled_send_time = Column(DateTime, nullable=True)
    recipient_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    message_content = Column(String, nullable=True)
    device_assignment = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_date = Column(DateTime, nullable=True)  # From Notion
    sent_date = Column(DateTime, nullable=True)  # When actually sent

    content = Column(JSON, nullable=True)  # Additional task-specific data
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    attempt_count = Column(Integer, default=0)
    error_message = Column(String, nullable=True)

    # Relationship
    device = relationship("Device", back_populates="tasks")
    logs = relationship("Log", back_populates="task")


class Log(Base):
    """Log model - represents an action log entry"""
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    device_id = Column(String, ForeignKey('devices.id'), nullable=True)
    task_id = Column(String, ForeignKey('tasks.id'), nullable=True)
    action = Column(String, nullable=False)  # e.g., "whatsapp_send", "device_connect"
    status = Column(String, nullable=False)  # success, failed, warning, info
    duration_seconds = Column(Float, nullable=True)
    error_message = Column(String, nullable=True)
    screenshot_path = Column(String, nullable=True)
    extra_data = Column(JSON, nullable=True)  # Additional structured data

    # Relationships
    device = relationship("Device", back_populates="logs")
    task = relationship("Task", back_populates="logs")


class Scenario(Base):
    """Scenario model - represents an automation workflow"""
    __tablename__ = "scenarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default=ScenarioStatus.DRAFT.value)

    # Execution settings
    device_id = Column(String, ForeignKey('devices.id'), nullable=True)
    priority = Column(Integer, default=5)  # 1-10, higher = more important

    # Scheduling (CRON-like)
    cron_expression = Column(String(100), nullable=True)  # e.g., "0 9 * * *" = daily at 9am
    scheduled_at = Column(DateTime, nullable=True)  # One-time scheduled execution
    repeat_count = Column(Integer, default=0)  # 0 = unlimited
    current_repeat = Column(Integer, default=0)

    # Interval between messages (for campaigns)
    min_interval_seconds = Column(Integer, default=300)  # 5 minutes
    max_interval_seconds = Column(Integer, default=600)  # 10 minutes

    # Execution state
    current_step_index = Column(Integer, default=0)
    total_steps = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)

    # Results
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

    # Notion integration
    notion_campaign_id = Column(String, nullable=True)

    # Extra configuration
    config = Column(JSON, nullable=True)

    # Relationships
    device = relationship("Device", backref="scenarios")
    steps = relationship("ScenarioStep", back_populates="scenario",
                        order_by="ScenarioStep.order", cascade="all, delete-orphan")


class ScenarioStep(Base):
    """ScenarioStep model - represents a single step in a scenario"""
    __tablename__ = "scenario_steps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scenario_id = Column(String, ForeignKey('scenarios.id', ondelete='CASCADE'), nullable=False)

    # Step definition
    name = Column(String(200), nullable=False)
    agent_type = Column(String(50), nullable=False)  # whatsapp, instagram, etc.
    action = Column(String(100), nullable=False)  # send_message, post_reel, etc.
    order = Column(Integer, nullable=False)  # Execution order (1, 2, 3...)

    # Step configuration
    config = Column(JSON, nullable=True)  # Agent-specific parameters
    prompt_template_id = Column(String, nullable=True)  # Reference to prompt template

    # Execution state
    status = Column(String(20), default=StepStatus.PENDING.value)
    attempt_count = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)

    # Timing
    delay_before_seconds = Column(Integer, default=0)  # Wait before executing
    timeout_seconds = Column(Integer, default=300)  # 5 min timeout

    # Conditions
    condition = Column(JSON, nullable=True)  # e.g., {"previous_step": "success"}
    skip_on_failure = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Results
    result = Column(JSON, nullable=True)  # Step execution result
    error_message = Column(Text, nullable=True)

    # Relationship
    scenario = relationship("Scenario", back_populates="steps")


class ScheduledJob(Base):
    """ScheduledJob model - represents a scheduled task execution"""
    __tablename__ = "scheduled_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Job type
    job_type = Column(String(50), nullable=False)  # scenario, task, maintenance
    reference_id = Column(String, nullable=True)  # scenario_id or task_id

    # Scheduling
    cron_expression = Column(String(100), nullable=True)
    scheduled_at = Column(DateTime, nullable=True)

    # State
    is_active = Column(Boolean, default=True)
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    run_count = Column(Integer, default=0)

    # Config
    config = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Execution(Base):
    """Execution model - step-by-step execution log for scenarios"""
    __tablename__ = "executions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scenario_id = Column(String, ForeignKey('scenarios.id', ondelete='CASCADE'), nullable=False)
    step_id = Column(String, ForeignKey('scenario_steps.id', ondelete='SET NULL'), nullable=True)
    device_id = Column(String, ForeignKey('devices.id', ondelete='SET NULL'), nullable=True)

    # Execution details
    action = Column(String(100), nullable=False)  # send_whatsapp, send_sms, etc.
    target = Column(String, nullable=True)  # phone number, contact name
    status = Column(String(20), default="pending")  # pending, running, success, failed, skipped

    # Input/Output
    input_data = Column(JSON, nullable=True)  # Parameters passed to action
    output_data = Column(JSON, nullable=True)  # Result from action
    error_message = Column(Text, nullable=True)

    # Timing
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_ms = Column(Integer, nullable=True)

    # Screenshots
    screenshot_before = Column(String, nullable=True)  # Path to screenshot before action
    screenshot_after = Column(String, nullable=True)  # Path to screenshot after action

    # Retry tracking
    attempt_number = Column(Integer, default=1)
    max_attempts = Column(Integer, default=3)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    scenario = relationship("Scenario", backref="executions")
    step = relationship("ScenarioStep", backref="executions")
    device = relationship("Device", backref="executions")


class RateLimit(Base):
    """RateLimit model - per-device rate limiting configuration"""
    __tablename__ = "rate_limits"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String, ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)

    # Rate limit type
    limit_type = Column(String(50), nullable=False)  # whatsapp, sms, max, global
    channel = Column(String(50), nullable=True)  # Specific channel if applicable

    # Limits
    max_per_hour = Column(Integer, default=20)
    max_per_day = Column(Integer, default=100)
    min_interval_seconds = Column(Integer, default=60)  # Minimum time between messages

    # Current usage (reset daily/hourly)
    current_hour_count = Column(Integer, default=0)
    current_day_count = Column(Integer, default=0)
    last_action_at = Column(DateTime, nullable=True)
    hour_reset_at = Column(DateTime, nullable=True)
    day_reset_at = Column(DateTime, nullable=True)

    # State
    is_blocked = Column(Boolean, default=False)
    blocked_until = Column(DateTime, nullable=True)
    block_reason = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    device = relationship("Device", backref="rate_limits")


class UIPath(Base):
    """UIPath model - UIAutomator selectors for different apps/screens"""
    __tablename__ = "ui_paths"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # App identification
    app_name = Column(String(50), nullable=False)  # whatsapp, max, sms, telegram
    app_package = Column(String(100), nullable=True)  # com.whatsapp, etc.
    app_version = Column(String(20), nullable=True)  # Version this selector works for

    # Screen/Element identification
    screen_name = Column(String(100), nullable=False)  # main_chat, contact_search, etc.
    element_name = Column(String(100), nullable=False)  # send_button, message_input, etc.

    # Selectors (multiple strategies)
    resource_id = Column(String, nullable=True)  # Android resource ID
    content_desc = Column(String, nullable=True)  # Content description
    xpath = Column(String, nullable=True)  # XPath selector
    class_name = Column(String, nullable=True)  # Android class name
    text_pattern = Column(String, nullable=True)  # Text or regex pattern
    bounds = Column(String, nullable=True)  # Fallback coordinates [x1,y1,x2,y2]

    # Selector metadata
    selector_priority = Column(Integer, default=1)  # Lower = try first
    is_active = Column(Boolean, default=True)
    confidence = Column(Float, default=1.0)  # How reliable this selector is (0-1)

    # Usage tracking
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    last_success_at = Column(DateTime, nullable=True)
    last_failure_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SessionCache(Base):
    """SessionCache model - cached app session data for faster automation"""
    __tablename__ = "session_cache"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String, ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)

    # Cache type
    cache_type = Column(String(50), nullable=False)  # app_state, contact_list, recent_chats
    app_name = Column(String(50), nullable=True)

    # Cached data
    data = Column(JSON, nullable=False)

    # Validity
    expires_at = Column(DateTime, nullable=True)
    is_valid = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    device = relationship("Device", backref="session_caches")


# ============================================
# WORKFLOW MODELS (Visual Builder)
# ============================================

class WorkflowStatus(str, enum.Enum):
    """Workflow status"""
    DRAFT = "draft"
    ACTIVE = "active"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class Workflow(Base):
    """Workflow model - visual workflow with nodes and edges (ReactFlow)"""
    __tablename__ = "workflows"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default=WorkflowStatus.DRAFT.value)

    # Execution settings
    device_id = Column(String, ForeignKey('devices.id'), nullable=True)

    # Statistics
    run_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    last_run_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    device = relationship("Device", backref="workflows")
    nodes = relationship("WorkflowNode", back_populates="workflow",
                        cascade="all, delete-orphan")
    edges = relationship("WorkflowEdge", back_populates="workflow",
                        cascade="all, delete-orphan")


class WorkflowNode(Base):
    """WorkflowNode model - single node in a visual workflow (ReactFlow node)"""
    __tablename__ = "workflow_nodes"

    id = Column(String, primary_key=True)  # ReactFlow node ID
    workflow_id = Column(String, ForeignKey('workflows.id', ondelete='CASCADE'), nullable=False)

    # Node type (trigger, action, condition)
    node_type = Column(String(50), nullable=False)

    # Position on canvas
    position_x = Column(Float, nullable=False, default=0)
    position_y = Column(Float, nullable=False, default=0)

    # Node data (label, description, agent, icon, config, etc.)
    data = Column(JSON, nullable=False, default=dict)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    workflow = relationship("Workflow", back_populates="nodes")


class WorkflowEdge(Base):
    """WorkflowEdge model - connection between nodes (ReactFlow edge)"""
    __tablename__ = "workflow_edges"

    id = Column(String, primary_key=True)  # ReactFlow edge ID
    workflow_id = Column(String, ForeignKey('workflows.id', ondelete='CASCADE'), nullable=False)

    # Source and target nodes
    source_node_id = Column(String, nullable=False)
    target_node_id = Column(String, nullable=False)

    # Handle IDs for condition nodes (yes/no branches)
    source_handle = Column(String(50), nullable=True)
    target_handle = Column(String(50), nullable=True)

    # Edge appearance
    label = Column(String(100), nullable=True)
    animated = Column(Boolean, default=False)
    style = Column(JSON, nullable=True)  # {stroke: '#color', strokeWidth: 2}

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    workflow = relationship("Workflow", back_populates="edges")
