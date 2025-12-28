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
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TELEGRAM = "telegram"
    YOUTUBE = "youtube"
    SMS = "sms"
    NOTION = "notion"
    SCRAPER = "scraper"


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
