from pathlib import Path

from typer.testing import CliRunner

from ici.cli import app


def test_collect_command_exits_successfully_and_writes_output(monkeypatch) -> None:
    project_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(project_root)

    output_path = project_root / "reports" / "company_master.csv"
    if output_path.exists():
        output_path.unlink()

    runner = CliRunner()
    result = runner.invoke(app, ["collect"])

    assert result.exit_code == 0
    assert "Starting company master collection..." in result.stdout
    assert "Collection completed successfully." in result.stdout
    assert "Companies collected:" in result.stdout
    assert "Output: reports/company_master.csv" in result.stdout
    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")
    assert content.count("\n") >= 2
    assert "RELIANCE" in content or "TCS" in content
