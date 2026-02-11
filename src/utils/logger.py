"""
Logger configuration for TAI-EvalGenTCS CLI.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: Optional[str] = None,
    verbose: bool = False,
    log_level: Optional[str] = None
) -> logging.Logger:
    """
    Setup and configure logger with timestamps and configurable levels.
    
    Args:
        name: Logger name (defaults to root logger)
        verbose: Enable verbose (DEBUG) logging
        log_level: Log level as string ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
                  Overrides verbose parameter if provided
    
    Returns:
        Configured logger instance
    """
    # Get logger
    logger = logging.getLogger(name)
    
    # Determine log level
    if log_level:
        # Convert string to logging level
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {log_level}')
        level = numeric_level
    else:
        level = logging.DEBUG if verbose else logging.INFO
    
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter with timestamp
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger
