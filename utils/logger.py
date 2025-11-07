"""Centralized logging configuration for DOF Chat application."""

import logging
import sys


def setup_logger() -> logging.Logger:
    """Setup application logger with console output."""
    logger = logging.getLogger('dof_chat')
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s'
        ))
        logger.addHandler(handler)
    
    return logger


# Global logger instance
logger = setup_logger()