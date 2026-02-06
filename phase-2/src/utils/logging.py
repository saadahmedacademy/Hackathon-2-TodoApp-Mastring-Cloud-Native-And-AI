"""Logging configuration for the todo application."""
import logging
import os
from datetime import datetime
from typing import Optional

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to stdout
    ]
)

# Create a logger for the todo application
logger = logging.getLogger('todo_app')

# Set level based on environment
if os.getenv('DEBUG', 'False').lower() == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


def log_info(message: str, extra: Optional[dict] = None):
    """Log an info message."""
    if extra:
        logger.info(message, extra=extra)
    else:
        logger.info(message)


def log_error(message: str, extra: Optional[dict] = None):
    """Log an error message."""
    if extra:
        logger.error(message, extra=extra)
    else:
        logger.error(message)


def log_debug(message: str, extra: Optional[dict] = None):
    """Log a debug message."""
    if extra:
        logger.debug(message, extra=extra)
    else:
        logger.debug(message)


def log_warning(message: str, extra: Optional[dict] = None):
    """Log a warning message."""
    if extra:
        logger.warning(message, extra=extra)
    else:
        logger.warning(message)


def get_logger(name: str):
    """Get a named logger instance."""
    return logging.getLogger(f'todo_app.{name}')