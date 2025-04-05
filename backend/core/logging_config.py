import os
import sys
import json
from pathlib import Path
from pydantic import BaseModel

from loguru import logger

from .config import settings


class LogConfig(BaseModel):
    """
    Configuration model for Loguru logging setup.
    
    This model uses Pydantic for validation and provides default values
    from application settings. It centralizes all logging-related configuration
    in one place for easier management.
    """
    
    # Log levels in increasing order of severity:
    # TRACE: Detailed debug information (even more granular than DEBUG)
    # DEBUG: Debugging information during development
    # INFO: Confirmation that things are working as expected
    # SUCCESS: Successful completion of significant operations
    # WARNING: Indicate potential issues that don't prevent execution
    # ERROR: Errors that prevent specific operations from functioning
    # CRITICAL: Critical errors that may cause application failure
    LOG_LEVEL: str = settings.LOG_LEVEL
    
    # Log formats:
    # - "simple": Human-readable colored output for console and plain text for files
    # - "json": Structured JSON format for machine parsing and analysis
    LOG_FORMAT: str = settings.LOG_FORMAT
    
    # File logging settings
    LOG_FILE_PATH: str = settings.LOG_FILE_PATH  # Path to log file
    LOG_ROTATION: str = settings.LOG_ROTATION    # When to rotate logs (size or time)
    LOG_RETENTION: str = settings.LOG_RETENTION  # How long to keep old logs


def format_record(record):
    """
    Format log record as JSON for structured logging.
    
    Creates a consistent JSON structure for each log entry, making logs
    easier to parse, search, and analyze with tools like ELK stack.
    Required for the "json" log format option.
    
    Args:
        record: Loguru record object containing log data
        
    Returns:
        Formatted JSON string representing the log entry
    """
    # Format the message with essential fields
    log_dict = {
        "time": record["time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
        "level": record["level"].name,
        "message": record["message"],
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
    }
    
    # Add exception info if present
    if record["exception"]:
        log_dict["exception"] = record["exception"]
        
    # Add extra attributes from structured logging
    # Usage: logger.bind(request_id="123").info("Processing request")
    for key, value in record["extra"].items():
        log_dict[key] = value
    
    return json.dumps(log_dict)


def setup_logging():
    """
    Configure Loguru logger with console and file handlers.
    
    This function:
    1. Removes default Loguru configuration
    2. Adds console output with appropriate formatting
    3. Creates log directory if it doesn't exist
    4. Adds file logging with rotation and retention policies
    
    The configured logger supports both simple human-readable format and
    structured JSON logging based on configuration. It also includes features
    like log rotation, compression, and exception tracing.
    
    Usage examples:
        ```python
        # Basic logging
        from loguru import logger
        logger.info("Application started")
        
        # Logging with context data
        logger.bind(user_id=123).info("User logged in")
        
        # Error logging with exception information
        try:
            # Some code
        except Exception as e:
            logger.exception(f"Error occurred: {e}")
        ```
    
    Returns:
        Configured logger instance
    """
    config = LogConfig()
    
    # First, remove default logger
    logger.remove()
    
    # Add console logger
    if config.LOG_FORMAT.lower() == "json":
        # JSON format for structured logging and machine processing
        logger.add(
            sys.stderr,
            level=config.LOG_LEVEL,
            format=format_record,
            colorize=False,  # No color in JSON mode
            backtrace=True,  # Show trace for exceptions
            diagnose=True,   # Include variable values in tracebacks
        )
    else:
        # Simple human-readable format with colors for console
        logger.add(
            sys.stderr,
            level=config.LOG_LEVEL,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            colorize=True,   # Color output for readability
            backtrace=True,  # Show trace for exceptions
            diagnose=True,   # Include variable values in tracebacks
        )
    
    # Create log directory if it doesn't exist
    log_path = Path(config.LOG_FILE_PATH)
    log_dir = log_path.parent
    os.makedirs(log_dir, exist_ok=True)
    
    # Add file logger
    if config.LOG_FORMAT.lower() == "json":
        # JSON format for file logging (machine-readable)
        logger.add(
            config.LOG_FILE_PATH,
            level=config.LOG_LEVEL,
            format=format_record,
            rotation=config.LOG_ROTATION,     # Rotate logs based on size or time
            retention=config.LOG_RETENTION,   # Cleanup old logs automatically
            compression="zip",                # Compress rotated logs
            backtrace=True,                   # Show trace for exceptions
            diagnose=True,                    # Include variable values in tracebacks
        )
    else:
        # Simple format for file logging (without colors)
        logger.add(
            config.LOG_FILE_PATH,
            level=config.LOG_LEVEL,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} - {message}",
            rotation=config.LOG_ROTATION,     # Rotate logs based on size or time
            retention=config.LOG_RETENTION,   # Cleanup old logs automatically
            compression="zip",                # Compress rotated logs
            backtrace=True,                   # Show trace for exceptions
            diagnose=True,                    # Include variable values in tracebacks
        )
    
    logger.info(f"Logging initialized with level {config.LOG_LEVEL}")
    return logger 