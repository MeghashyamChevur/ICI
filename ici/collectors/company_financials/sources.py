"""Source abstractions and implementations for the company financials collector."""

from __future__ import annotations

import csv
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .exceptions import (
    CompanyFinancialsDecodeError,
    CompanyFinancialsDownloadError,
)


@dataclass(slots=True)
class CompanyFinancialsSource(ABC):
    """Abstract interface for company financial data sources."""

    name: str = "company_financials"
    description: str = "Source for company financial metrics"

    @abstractmethod
    def fetch(self) -> Any:
        """Fetch financial records."""

    @abstractmethod
    def download(self) -> bytes:
        """Download the raw payload."""


@dataclass(slots=True)
class FileCompanyFinancialsSource(CompanyFinancialsSource):
    """Read company financial records from a CSV file."""

    path: Path | None = None

    def download(self) -> bytes:
        """Return the raw CSV file contents."""
        file_path = self.path or Path("tests/data/company_financials_sample.csv")

        if not file_path.exists():
            raise CompanyFinancialsDownloadError(
                f"Financial sample file not found: {file_path}"
            )

        return file_path.read_bytes()

    def fetch(self) -> dict[str, list[dict[str, Any]]]:
        """Load and decode the CSV into parser-friendly payload."""
        raw_payload = self.download()
        return self._decode_payload(raw_payload)

    def _decode_payload(self, payload: bytes) -> dict[str, list[dict[str, Any]]]:
        """Decode CSV payload into a records dictionary."""
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CompanyFinancialsDecodeError(
                "Failed to decode financial payload"
            ) from exc

        reader = csv.DictReader(text.splitlines())

        records: list[dict[str, Any]] = []

        for row in reader:
            if row:
                records.append(
                    {key: value for key, value in row.items() if key is not None}
                )

        return {"records": records}


class CompanyFinancialsSourceFactory:
    """Create financial source implementations."""

    def create(
        self,
        *,
        path: Path | None = None,
    ) -> CompanyFinancialsSource:
        """Return the default file-backed source."""
        return FileCompanyFinancialsSource(
            path=path or Path("tests/data/company_financials_sample.csv")
        )


def get_default_company_financials_source() -> CompanyFinancialsSource:
    """Return the default financial source."""
    return CompanyFinancialsSourceFactory().create()