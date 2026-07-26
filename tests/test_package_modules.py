from pathlib import Path

from typer.testing import CliRunner

from ici.cli import app
from ici.config import get_project_paths, initialize_project_structure
from ici.logger import get_logger
from ici.settings import Settings
from ici.utils import current_timestamp, ensure_directory, load_json, save_json


def test_project_paths_are_created() -> None:
    paths = get_project_paths()
    assert paths["data_raw"].name == "raw"
    assert paths["reports"].name == "reports"
    assert paths["tests"].name == "tests"


def test_initialize_project_structure_creates_directories(tmp_path: Path) -> None:
    base_dir = tmp_path / "demo_project"
    initialize_project_structure(base_dir)
    assert (base_dir / "data" / "raw").exists()
    assert (base_dir / "logs").exists()
    assert (base_dir / "scripts" / "extract").exists()


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.application_name == "ICI"
    assert settings.version == "0.1.0"
    assert settings.default_currency == "INR"


def test_logger_can_be_created() -> None:
    logger = get_logger("test-module")
    assert logger.name == "test-module"


def test_utils_handle_json_round_trip(tmp_path: Path) -> None:
    target_dir = tmp_path / "json-output"
    ensure_directory(target_dir)
    payload = {"status": "ok"}
    save_json(target_dir / "sample.json", payload)
    loaded = load_json(target_dir / "sample.json")
    assert loaded == payload


def test_cli_status_command() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Status" in result.stdout


def test_current_timestamp_is_string() -> None:
    stamp = current_timestamp()
    assert isinstance(stamp, str)
    assert len(stamp) > 0
