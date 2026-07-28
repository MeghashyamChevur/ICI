"""Orchestration layer for the company financials collector pipeline."""

from __future__ import annotations

from typing import Any

from ..base import BaseCollector
from ...models.company_financials import CompanyFinancials
from .normalizer import CompanyFinancialsNormalizer
from .parser import CompanyFinancialsParser
from .persistence import CompanyFinancialsPersistence
from .sources import (
    CompanyFinancialsSource,
    get_default_company_financials_source,
)


class CompanyFinancialsCollector(BaseCollector[CompanyFinancials]):
    """Coordinate the company financials workflow through injected collaborators."""

    name = "company_financials"

    def __init__(
        self,
        source: CompanyFinancialsSource | None = None,
        parser: CompanyFinancialsParser | None = None,
        normalizer: CompanyFinancialsNormalizer | None = None,
        persistence: CompanyFinancialsPersistence | None = None,
        validator: Any | None = None,
    ) -> None:
        """Initialize the collector with its collaborators."""
        self.source = source or get_default_company_financials_source()
        self.parser = parser or CompanyFinancialsParser()
        self.normalizer = normalizer or CompanyFinancialsNormalizer()
        self.persistence = persistence or CompanyFinancialsPersistence()
        self.validator = validator

    def collect(self) -> list[CompanyFinancials]:
        """Collect and return the validated financial records."""
        payload = self.download()
        parsed_records = self.parse(payload)
        normalized_records = self.normalize(parsed_records)
        validated_records = self.validate_many(normalized_records)
        self.save(validated_records)
        return validated_records

    def validate(self, item: CompanyFinancials) -> bool:
        """Validate a financial record using the configured validator or default rule."""
        if self.validator is not None:
            self.validator.validate(item)
            return True
        return bool(item.symbol)

    def validate_many(
        self,
        items: list[CompanyFinancials],
    ) -> list[CompanyFinancials]:
        """Validate a collection of financial records."""
        validated: list[CompanyFinancials] = []

        for item in items:
            if self.validate(item):
                validated.append(item)

        return validated

    def download(self) -> Any:
        """Download the raw financial payload."""
        return self.source.fetch()

    def parse(self, payload: Any) -> list[CompanyFinancials]:
        """Parse the raw payload into CompanyFinancials objects."""
        return self.parser.parse(payload)

    def normalize(
        self,
        items: list[CompanyFinancials],
    ) -> list[CompanyFinancials]:
        """Normalize financial records."""
        return self.normalizer.normalize_many(items)

    def save(self, items: list[CompanyFinancials]) -> None:
        """Persist the validated financial records."""
        self.persistence.save(items)