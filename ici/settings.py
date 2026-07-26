"""Typed application settings for the ICI package."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    """Configuration container for application-wide defaults."""

    application_name: str = "ICI"
    version: str = "0.1.0"
    default_currency: str = "INR"
    financial_year_start_month: int = 4
    logging_level: str = "INFO"
    excel_output_directory: str = "excel"
    raw_data_directory: str = "data/raw"
    processed_data_directory: str = "data/processed"
