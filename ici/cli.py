"""Command-line interface for the ICI package."""

from __future__ import annotations

from pathlib import Path

import typer

from .collectors.company_master.collector import CompanyMasterCollector
from .collectors.company_master.normalizer import CompanyMasterNormalizer
from .collectors.company_master.parser import CompanyMasterParser
from .collectors.company_master.persistence import CompanyMasterPersistence
from .collectors.company_master.sources import FileCompanyMasterSource
from .collectors.company_master.validator import CompanyMasterValidator

from .collectors.company_financials.collector import CompanyFinancialsCollector
from .collectors.company_financials.normalizer import CompanyFinancialsNormalizer
from .collectors.company_financials.parser import CompanyFinancialsParser
from .collectors.company_financials.persistence import CompanyFinancialsPersistence
from .collectors.company_financials.sources import FileCompanyFinancialsSource
from .collectors.company_financials.validator import CompanyFinancialsValidator

from .logger import get_logger

app = typer.Typer(help="Indian Compounder Index command-line interface")
logger = get_logger("ici.cli")


class _CliFileCompanyMasterSource(FileCompanyMasterSource):
    """Adapt the file-backed source to the payload shape expected by the parser."""

    def fetch(self) -> dict[str, list[dict[str, object]]]:
        records = super().fetch()
        return {"records": records}


class _CliFileCompanyFinancialsSource(FileCompanyFinancialsSource):
    """Use the financial sample source for the CLI."""

    def fetch(self) -> dict[str, list[dict[str, object]]]:
        return super().fetch()


@app.command()
def init() -> None:
    """Initialize the project structure."""
    logger.info("Running init command")
    typer.echo("Initialization complete. Project structure is ready.")


@app.command()
def status() -> None:
    """Show the current project status."""
    logger.info("Running status command")
    typer.echo("Status: project scaffold is configured and ready for future development.")


@app.command()
def collect() -> None:
    """Collect company master data from the sample dataset and write the output CSV."""
    logger.info("Running collect command")
    typer.echo("Starting company master collection...")

    source = _CliFileCompanyMasterSource(
        path=Path("tests/data/company_master_sample.csv")
    )
    parser = CompanyMasterParser()
    normalizer = CompanyMasterNormalizer()
    validator = CompanyMasterValidator()
    persistence = CompanyMasterPersistence(
        output_path=Path("reports/company_master.csv")
    )

    collector = CompanyMasterCollector(
        source=source,
        parser=parser,
        normalizer=normalizer,
        persistence=persistence,
        validator=validator,
    )

    companies = collector.collect()

    typer.echo("Collection completed successfully.")
    typer.echo(f"Companies collected: {len(companies)}")
    typer.echo("Output: reports/company_master.csv")


@app.command("collect-financials")
def collect_financials() -> None:
    """Collect company financial data from the sample dataset."""
    logger.info("Running collect-financials command")
    typer.echo("Starting company financials collection...")

    source = _CliFileCompanyFinancialsSource(
        path=Path("tests/data/company_financials_sample.csv")
    )
    parser = CompanyFinancialsParser()
    normalizer = CompanyFinancialsNormalizer()
    validator = CompanyFinancialsValidator()
    persistence = CompanyFinancialsPersistence(
        output_path=Path("reports/company_financials.csv")
    )

    collector = CompanyFinancialsCollector(
        source=source,
        parser=parser,
        normalizer=normalizer,
        persistence=persistence,
        validator=validator,
    )

    financials = collector.collect()

    typer.echo("Collection completed successfully.")
    typer.echo(f"Financial records collected: {len(financials)}")
    typer.echo("Output: reports/company_financials.csv")


@app.command()
def validate() -> None:
    """Validate collected data."""
    logger.info("Running validate command")
    typer.echo(
        "Validate command placeholder: validation workflow will be implemented later."
    )


@app.command()
def score() -> None:
    """Calculate scoring metrics."""
    logger.info("Running score command")
    typer.echo(
        "Score command placeholder: scoring workflow will be implemented later."
    )


@app.command()
def export() -> None:
    """Export results to the configured output formats."""
    logger.info("Running export command")
    typer.echo(
        "Export command placeholder: export workflow will be implemented later."
    )


if __name__ == "__main__":
    app()