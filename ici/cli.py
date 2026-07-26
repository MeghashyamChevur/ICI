"""Command-line interface for the ICI package."""

from __future__ import annotations

import typer

from .logger import get_logger

app = typer.Typer(help="Indian Compounder Index command-line interface")
logger = get_logger("ici.cli")


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
    """Collect data from configured sources."""
    logger.info("Running collect command")
    typer.echo("Collect command placeholder: data collection workflow will be implemented later.")


@app.command()
def validate() -> None:
    """Validate collected data."""
    logger.info("Running validate command")
    typer.echo("Validate command placeholder: validation workflow will be implemented later.")


@app.command()
def score() -> None:
    """Calculate scoring metrics."""
    logger.info("Running score command")
    typer.echo("Score command placeholder: scoring workflow will be implemented later.")


@app.command()
def export() -> None:
    """Export results to the configured output formats."""
    logger.info("Running export command")
    typer.echo("Export command placeholder: export workflow will be implemented later.")


if __name__ == "__main__":
    app()
