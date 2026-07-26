"""Reusable helper functions for the ICI package."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def ensure_directory(path: str | Path) -> Path:
    """Create a directory and return its path."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def current_timestamp() -> str:
    """Return a UTC timestamp suitable for logs and filenames."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: str | Path) -> Any:
    """Load a JSON document from disk."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: str | Path, payload: Any) -> Path:
    """Persist a Python object as JSON to disk."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return file_path
