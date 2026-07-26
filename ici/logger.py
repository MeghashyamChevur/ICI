"""Logging setup for the ICI package."""

from __future__ import annotations

import logging
from pathlib import Path

from .config import initialize_project_structure
from .utils import ensure_directory


LOG_FILE = Path("logs") / "ici.log"


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Create or return a configured logger instance."""
    initialize_project_structure()
    ensure_directory(Path("logs"))

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
