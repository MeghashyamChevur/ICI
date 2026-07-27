"""Source abstractions and implementations for the company master collector."""

from __future__ import annotations

import csv
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

from .exceptions import CompanyMasterSourceDecodeError, CompanyMasterSourceDownloadError


@dataclass(slots=True)
class CompanyMasterSource(ABC):
    """Abstract interface for any company master data source."""

    name: str = "company_master"
    url: str = ""
    format: str = "json"
    description: str = "Placeholder source definition for the company master collector"

    @abstractmethod
    def fetch(self) -> Any:
        """Fetch the raw payload from the source.

        The implementation is intentionally placeholder-based for now and should
        return a structure that the parser can consume.
        """

    @abstractmethod
    def download(self) -> Any:
        """Return a placeholder download payload for the source.

        This method exists to keep the source abstraction dependency-injection
        friendly and to reserve the download step for a future implementation.
        """


@dataclass(slots=True)
class NseCompanyMasterSource(CompanyMasterSource):
    """Placeholder implementation for the primary NSE company master source."""

    name: str = "nse_company_master"
    url: str = "https://example.com/nse/company-master"
    format: str = "json"
    description: str = "Placeholder NSE source for company master data"
    session: requests.Session | None = None

    def download(self) -> bytes:
        """Download the raw response body from the configured source."""
        if self.session is None:
            return b'{"source": "nse_company_master", "records": []}'

        session = self.session
        try:
            response = session.get(self.url, timeout=10)
        except requests.RequestException as exc:
            raise CompanyMasterSourceDownloadError(f"Failed to download company master data: {exc}") from exc
        except Exception as exc:  # pragma: no cover - defensive guard for mock-based tests
            raise CompanyMasterSourceDownloadError(f"Failed to download company master data: {exc}") from exc

        if response.status_code >= 400:
            raise CompanyMasterSourceDownloadError(
                f"Failed to download company master data: HTTP {response.status_code}"
            )

        return response.content

    def fetch(self) -> list[dict[str, Any]]:
        """Download, decode, and return iterable raw records for the parser."""
        raw_payload = self.download()
        return self._decode_payload(raw_payload)

    def _decode_payload(self, payload: bytes) -> list[dict[str, Any]]:
        """Decode the raw response payload into a list of record dictionaries."""
        try:
            decoded = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CompanyMasterSourceDecodeError("Failed to decode company master payload") from exc

        if not isinstance(decoded, dict):
            raise CompanyMasterSourceDecodeError("Decoded company master payload is not an object")

        records = decoded.get("records", [])
        if not isinstance(records, list):
            raise CompanyMasterSourceDecodeError("Decoded company master payload does not contain a records list")

        normalized_records: list[dict[str, Any]] = []
        for record in records:
            if isinstance(record, dict):
                normalized_records.append(record)
            else:
                raise CompanyMasterSourceDecodeError("Decoded company master payload contains a non-object record")
        return normalized_records


@dataclass(slots=True)
class FileCompanyMasterSource(CompanyMasterSource):
    """Read company master records from a CSV file on disk."""

    name: str = "file_company_master"
    url: str = ""
    format: str = "csv"
    description: str = "File-backed company master source for sample datasets"
    path: Path | None = None

    def download(self) -> bytes:
        """Return the raw contents of the backing CSV file as bytes."""
        file_path = self.path or Path("tests/data/company_master_sample.csv")
        if not file_path.exists():
            raise CompanyMasterSourceDownloadError(f"Company master sample file not found: {file_path}")
        return file_path.read_bytes()

    def fetch(self) -> list[dict[str, Any]]:
        """Load and decode the CSV file into raw record dictionaries."""
        raw_payload = self.download()
        return self._decode_payload(raw_payload)

    def _decode_payload(self, payload: bytes) -> list[dict[str, Any]]:
        """Decode CSV payload content into a list of record dictionaries."""
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CompanyMasterSourceDecodeError("Failed to decode company master payload") from exc

        reader = csv.DictReader(text.splitlines())
        records: list[dict[str, Any]] = []
        for row in reader:
            if not row:
                continue
            records.append({key: value for key, value in row.items() if key is not None})
        return records


class CompanyMasterSourceFactory:
    """Create a CompanyMasterSource implementation by simple selector."""

    def create(self, source_type: str, *, path: Path | None = None) -> CompanyMasterSource:
        """Return a source instance for the requested implementation type."""
        normalized = (source_type or "file").strip().lower()
        if normalized == "nse":
            return NseCompanyMasterSource()
        if normalized == "file":
            return FileCompanyMasterSource(path=path or Path("tests/data/company_master_sample.csv"))
        raise ValueError(f"Unsupported company master source type: {source_type}")


def get_default_company_master_source() -> CompanyMasterSource:
    """Return the default source implementation used by the collector."""
    return CompanyMasterSourceFactory().create("file")
