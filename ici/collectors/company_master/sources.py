"""Source abstractions and placeholder implementations for the company master collector."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


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


@dataclass(slots=True)
class NseCompanyMasterSource(CompanyMasterSource):
    """Placeholder implementation for the primary NSE company master source."""

    name: str = "nse_company_master"
    url: str = "https://example.com/nse/company-master"
    format: str = "json"
    description: str = "Placeholder NSE source for company master data"

    def fetch(self) -> dict[str, Any]:
        """Return placeholder data without making any network requests."""
        return {
            "source": self.name,
            "records": [],
        }


def get_default_company_master_source() -> CompanyMasterSource:
    """Return the default source implementation used by the collector."""
    return NseCompanyMasterSource()
