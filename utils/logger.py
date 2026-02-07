"""
Privacy-aware logging system for MoltMobo
Redacts sensitive information from logs
"""

import logging
import re
from pathlib import Path
from logging.handlers import RotatingFileHandler
import colorlog

# Sensitive patterns to redact
SENSITIVE_PATTERNS = [
    (r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD_REDACTED]'),  # Credit cards
    (r'\b\d{6}\b', '[OTP_REDACTED]'),  # OTP codes
    (r'password["\s:=]+[\w\S]+', 'password=[REDACTED]'),  # Passwords
    (r'api[_-]?key["\s:=]+[\w\S]+', 'api_key=[REDACTED]'),  # API keys
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),  # Emails
]


class PrivacyFilter(logging.Filter):
    """Filter that redacts sensitive information from log messages"""
    
    def filter(self, record):
        if hasattr(record, 'msg'):
            msg = str(record.msg)
            for pattern, replacement in SENSITIVE_PATTERNS:
                msg = re.sub(pattern, replacement, msg, flags=re.IGNORECASE)
            record.msg = msg
        return True


def setup_logger(name: str = "moltmobo", log_file: str = None, level: str = "INFO"):
    """
    Setup logger with console and file handlers
    
    Args:
        name: Logger name
        log_file: Path to log file (optional)
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with colors
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_format = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_format)
    console_handler.addFilter(PrivacyFilter())
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        file_handler.addFilter(PrivacyFilter())
        logger.addHandler(file_handler)
    
    return logger


class ActionLogger:
    """Specialized logger for action audit trail"""
    
    def __init__(self, log_file: str = "./logs/actions.log"):
        self.logger = setup_logger("actions", log_file, "INFO")
    
    def log_action(self, action_type: str, details: dict, success: bool = True):
        """
        Log an action with details
        
        Args:
            action_type: Type of action (tap, swipe, input, etc.)
            details: Dictionary with action details
            success: Whether action succeeded
        """
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"[{status}] {action_type}: {details}")
    
    def log_policy_violation(self, app_package: str, reason: str):
        """Log policy violation attempts"""
        self.logger.warning(f"POLICY VIOLATION: {app_package} - {reason}")
    
    def log_privacy_decision(self, decision: str, reason: str):
        """Log privacy routing decisions"""
        self.logger.info(f"PRIVACY: {decision} - {reason}")


# Global logger instance
logger = setup_logger()
action_logger = ActionLogger()
