"""
logger_config.py - Centralized logging setup for the Visitor Management System.

Creates a logger that logs:
- To both console and a persistent `logs/server.log` file
- With a consistent format and INFO-level by default
"""

import os
import logging
# from logging.handlers import RotatingFileHandler  # Optional: for log rotation

def setup_logger() -> logging.Logger:
    """
    Sets up and returns a logger instance configured for the application.

    - Logs INFO and above level messages
    - Outputs to both terminal and 'logs/server.log'
    - Creates 'logs' directory if it doesn't exist
    """
    os.makedirs("logs", exist_ok=True)

    # Optional: Use rotating file handler if log size becomes an issue
    # file_handler = RotatingFileHandler("logs/server.log", maxBytes=5_000_000, backupCount=5)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/server.log"),
            logging.StreamHandler()
            # file_handler
        ]
    )

    return logging.getLogger("visitor-management")
