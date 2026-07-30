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

from .collectors.company_intelligence import CompanyIntelligenceCollector
from .collectors.company_screening import CompanyScreeningCollector
from .collectors.company_ranking import CompanyRankingCollector

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
    typer.echo(
        "Status: project scaffold is configured and ready for future development."
    )


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


@app.command("collect-company-intelligence")
def collect_company_intelligence() -> None:
    """Build company intelligence by combining company and financial data."""
    logger.info("Running collect-company-intelligence command")
    typer.echo("Starting company intelligence collection...")

    collector = CompanyIntelligenceCollector(
        company_master_path=Path("reports/company_master.csv"),
        company_financials_path=Path("reports/company_financials.csv"),
        output_path=Path("reports/company_intelligence.json"),
    )

    intelligence = collector.collect()

    typer.echo("Collection completed successfully.")
    typer.echo(
        f"Company intelligence records created: {len(intelligence)}"
    )
    typer.echo("Output: reports/company_intelligence.json")


@app.command("screen-companies")
def screen_companies() -> None:
    """Screen companies using company intelligence."""

    logger.info("Running screen-companies command")
    typer.echo("Starting company screening...")

    collector = CompanyScreeningCollector(
        company_intelligence_path=Path(
            "reports/company_intelligence.json"
        ),
        output_path=Path(
            "reports/screened_companies.json"
        ),
    )

    companies = collector.collect()

    typer.echo("Screening completed successfully.")
    typer.echo(
        f"Qualified companies found: {len(companies)}"
    )
    typer.echo(
        "Output: reports/screened_companies.json"
    )

@app.command("rank-companies")
def rank_companies() -> None:
    """Rank qualified companies."""

    logger.info("Running rank-companies command")
    typer.echo("Starting company ranking...")

    collector = CompanyRankingCollector(
        screened_companies_path=Path(
            "reports/screened_companies.json"
        ),
        output_path=Path(
            "reports/ranked_companies.json"
        ),
    )

    companies = collector.collect()

    typer.echo("Ranking completed successfully.")
    typer.echo(
        f"Ranked companies: {len(companies)}"
    )
    typer.echo(
        "Output: reports/ranked_companies.json"
    )

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