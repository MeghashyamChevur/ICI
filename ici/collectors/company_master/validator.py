"""Validation utilities for company master records."""

from __future__ import annotations

import re
from typing import Any

from ...models.company import Company
from .exceptions import CompanyMasterValidationError


class CompanyMasterValidator:
    """Validate Company model instances without modifying them."""

    _VALID_EXCHANGES = {"NSE", "BSE", "BOTH"}
    _VALID_LISTING_STATUSES = {"Active", "Delisted"}
    _ISIN_PATTERN = re.compile(r"^[A-Z]{2}[A-Z0-9]{9}[0-9]{1}$")

    def validate_many(self, companies: list[Company]) -> list[Company]:
        """Validate a collection of companies and return the validated list."""
        validated: list[Company] = []
        for index, company in enumerate(companies):
            self._validate_company(company, index=index)
            validated.append(company)
        return validated

    def validate(self, company: Company) -> Company:
        """Validate a single company and return it if valid."""
        self._validate_company(company)
        return company

    def _validate_company(self, company: Company, *, index: int | None = None) -> None:
        """Validate the fields of a single company record."""
        prefix = f"Record {index}: " if index is not None else ""

        if not company.symbol or not str(company.symbol).strip():
            raise CompanyMasterValidationError(f"{prefix}symbol is required")

        if not company.company_name or not str(company.company_name).strip():
            raise CompanyMasterValidationError(f"{prefix}company_name is required")

        if company.isin is not None and not self._is_valid_isin(company.isin):
            raise CompanyMasterValidationError(f"{prefix}isin is invalid")

        if company.exchange is not None and not self._is_valid_exchange(company.exchange):
            raise CompanyMasterValidationError(f"{prefix}exchange is invalid")

        if company.listing_status is not None and not self._is_valid_listing_status(company.listing_status):
            raise CompanyMasterValidationError(f"{prefix}listing_status is invalid")

    def _is_valid_isin(self, value: Any) -> bool:
        """Validate an ISIN value when provided."""
        if value is None:
            return True
        return bool(self._ISIN_PATTERN.fullmatch(str(value).strip().upper()))

    def _is_valid_exchange(self, value: Any) -> bool:
        """Validate an exchange value when provided."""
        if value is None:
            return True
        normalized = str(value).strip().upper()
        return normalized in self._VALID_EXCHANGES

    def _is_valid_listing_status(self, value: Any) -> bool:
        """Validate a listing status value when provided."""
        if value is None:
            return True
        normalized = str(value).strip().lower()
        if normalized in {"active", "listed"}:
            return True
        if normalized in {"delisted", "inactive", "suspended"}:
            return True
        return False
