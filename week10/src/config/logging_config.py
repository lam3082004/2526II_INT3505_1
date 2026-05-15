import logging
import logging.handlers
import os
from pythonjsonlogger import jsonlogger


def setup_logging(log_level: str = "INFO") -> None:
    os.makedirs("logs", exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))

    # JSON file handler (rotating)
    json_handler = logging.handlers.RotatingFileHandler(
        "logs/app.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
    )
    json_handler.setFormatter(jsonlogger.JsonFormatter())
    root_logger.addHandler(json_handler)

    # Console handler (human-readable)
    console_handler = logging.StreamHandler()
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)

    # Audit logger
    audit_logger = logging.getLogger("audit")
    audit_handler = logging.handlers.RotatingFileHandler(
        "logs/audit.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    audit_handler.setFormatter(jsonlogger.JsonFormatter())
    audit_logger.addHandler(audit_handler)
    audit_logger.setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def get_audit_logger() -> logging.Logger:
    return logging.getLogger("audit")
