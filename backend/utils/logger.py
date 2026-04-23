import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # File Handler
    fh = RotatingFileHandler(
        log_dir / "app.log", maxBytes=10485760, backupCount=5
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # Add handlers
    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

app_logger = setup_logger("medical_scheduler")
