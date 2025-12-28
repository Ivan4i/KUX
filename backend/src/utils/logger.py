"""Logging configuration using loguru"""

from loguru import logger
import sys
from pathlib import Path


def setup_logger(log_level: str = "INFO"):
    """Configure logger with custom format and handlers"""

    # Remove default handler
    logger.remove()

    # Add console handler with colors
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level
    )

    # Create logs directory
    logs_dir = Path(__file__).parent.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Add file handler with rotation
    logger.add(
        logs_dir / "app_{time:YYYY-MM-DD}.log",
        rotation="00:00",  # Rotate at midnight
        retention="7 days",  # Keep logs for 7 days
        compression="zip",  # Compress old logs
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level
    )

    logger.info(f"Logger initialized with level: {log_level}")

    return logger
