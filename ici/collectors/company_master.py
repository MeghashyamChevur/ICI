"""Placeholder collector for company master data."""

from __future__ import annotations

from .base import BaseCollector
from ..models.company import Company


class CompanyMasterCollector(BaseCollector[Company]):
    """Placeholder collector for company master records."""

    name = "company_master"

    def collect(self) -> list[Company]:
        """Return an empty collection until a real source is implemented."""
        return []

    def validate(self, item: Company) -> bool:
        """Validate a company record using the default validator."""
        return bool(item.symbol and item.company_name)
