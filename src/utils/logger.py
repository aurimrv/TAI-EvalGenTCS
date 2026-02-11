"""
Logger configuration for TAI-EvalGenTCS CLI.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: Optional[str] = None,
    verbose: bool = False
) -> logging.Logger:
    """
    Setup and configure logger.
    
    Args:
        name: Logger name (defaults to root logger)
        verbose: Enable verbose (DEBUG) logging
    
    Returns:
        Configured logger instance
    """
    # Get logger
    logger = logging.getLogger(name)
    
    # Set level
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter
    if verbose:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
    
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger
