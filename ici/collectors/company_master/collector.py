"""Orchestration layer for the company master collector pipeline."""

from __future__ import annotations

from typing import Any

from ..base import BaseCollector
from ...models.company import Company
from .normalizer import CompanyMasterNormalizer
from .parser import CompanyMasterParser
from .persistence import CompanyMasterPersistence
from .sources import CompanyMasterSource, get_default_company_master_source


class CompanyMasterCollector(BaseCollector[Company]):
    """Coordinate the company master workflow through injected collaborators."""

    name = "company_master"

    def __init__(
        self,
        source: CompanyMasterSource | None = None,
        parser: CompanyMasterParser | None = None,
        normalizer: CompanyMasterNormalizer | None = None,
        persistence: CompanyMasterPersistence | None = None,
        validator: Any | None = None,
    ) -> None:
        """Initialize the collector with its collaborators."""
        self.source = source or get_default_company_master_source()
        self.parser = parser or CompanyMasterParser()
        self.normalizer = normalizer or CompanyMasterNormalizer()
        self.persistence = persistence or CompanyMasterPersistence()
        self.validator = validator

    def collect(self) -> list[Company]:
        """Collect and return the validated company records."""
        payload = self.download()
        parsed_records = self.parse(payload)
        normalized_records = self.normalize(parsed_records)
        validated_records = self.validate_many(normalized_records)
        self.save(validated_records)
        return validated_records

    def validate(self, item: Company) -> bool:
        """Validate a company record using the configured validator or default rule."""
        if self.validator is not None:
            self.validator.validate(item)
            return True
        return bool(item.symbol and item.company_name)

    def validate_many(self, items: list[Company]) -> list[Company]:
        """Validate a collection of companies and return the validated ones."""
        validated: list[Company] = []
        for item in items:
            if self.validate(item):
                validated.append(item)
        return validated

    def download(self) -> Any:
        """Download the raw company master payload from the configured source."""
        return self.source.fetch()

    def parse(self, payload: Any) -> list[Company]:
        """Parse the raw payload into Company objects through the parser collaborator."""
        return self.parser.parse(payload)

    def normalize(self, items: list[Company]) -> list[Company]:
        """Normalize Company objects through the normalizer collaborator."""
        return self.normalizer.normalize_many(items)

    def save(self, items: list[Company]) -> None:
        """Persist the validated companies using the configured persistence layer."""
        self.persistence.save(items)
