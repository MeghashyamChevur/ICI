"""Project configuration utilities for the ICI package."""

from __future__ import annotations

from pathlib import Path
from typing import Dict


ROOT_DIR = Path(__file__).resolve().parent.parent


def get_project_paths(base_dir: Path | None = None) -> Dict[str, Path]:
    """Return the canonical directory paths for the project."""
    root = base_dir or ROOT_DIR
    paths = {
        "root": root,
        "config": root / "config",
        "data": root / "data",
        "data_raw": root / "data" / "raw",
        "data_processed": root / "data" / "processed",
        "data_master": root / "data" / "master",
        "data_sources": root / "data" / "sources",
        "docs": root / "docs",
        "excel": root / "excel",
        "logs": root / "logs",
        "reports": root / "reports",
        "scripts": root / "scripts",
        "scripts_extract": root / "scripts" / "extract",
        "scripts_transform": root / "scripts" / "transform",
        "scripts_validate": root / "scripts" / "validate",
        "scripts_scoring": root / "scripts" / "scoring",
        "scripts_reports": root / "scripts" / "reports",
        "tests": root / "tests",
        "package": root / "ici",
    }
    return paths


def initialize_project_structure(base_dir: Path | None = None) -> Dict[str, Path]:
    """Create the project directories if they are missing."""
    paths = get_project_paths(base_dir)
    for path in paths.values():
        if path == paths["root"]:
            continue
        path.mkdir(parents=True, exist_ok=True)
    return paths


initialize_project_structure()
