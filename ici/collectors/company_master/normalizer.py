"""Normalization utilities for company master records."""

from __future__ import annotations

from ...models.company import Company


class CompanyMasterNormalizer:
    """Normalize Company domain objects without validating or persisting them."""

    def normalize_many(self, companies: list[Company]) -> list[Company]:
        """Normalize a collection of companies and return the transformed list."""
        return [self.normalize(company) for company in companies]

    def normalize(self, company: Company) -> Company:
        """Normalize a single company record in place via a new Company instance."""
        return Company(
            symbol=self._normalize_symbol(company.symbol),
            company_name=self._normalize_company_name(company.company_name),
            isin=self._normalize_optional_text(company.isin),
            nse_code=self._normalize_optional_text(company.nse_code),
            bse_code=self._normalize_optional_text(company.bse_code),
            sector=self._normalize_optional_text(company.sector),
            industry=self._normalize_optional_text(company.industry),
            exchange=self._normalize_exchange(company.exchange),
            listing_status=self._normalize_listing_status(company.listing_status),
            market_cap=company.market_cap,
            market_cap_category=self._normalize_optional_text(company.market_cap_category),
            listing_date=self._normalize_optional_text(company.listing_date),
            face_value=company.face_value,
            website=self._normalize_optional_text(company.website),
            headquarters=self._normalize_optional_text(company.headquarters),
            business_description=self._normalize_optional_text(company.business_description),
        )

    def _normalize_symbol(self, value: str) -> str:
        """Trim whitespace and standardize trading symbols to uppercase."""
        return str(value).strip().upper()

    def _normalize_company_name(self, value: str) -> str:
        """Normalize company names consistently without changing their meaning."""
        cleaned = str(value).strip()
        if not cleaned:
            return ""
        parts = cleaned.split()
        return " ".join(part for part in parts if part)

    def _normalize_optional_text(self, value: str | None) -> str | None:
        """Trim whitespace from optional text values while preserving empties."""
        if value is None:
            return None
        cleaned = str(value).strip()
        return cleaned or None

    def _normalize_exchange(self, value: str | None) -> str | None:
        """Normalize exchange values to a standard vocabulary."""
        if value is None:
            return None
        normalized = str(value).strip().upper()
        if normalized in {"NSE", "BSE", "BOTH"}:
            return "NSE" if normalized == "NSE" else ("BSE" if normalized == "BSE" else "BOTH")
        if normalized in {"N", "NATIONAL STOCK EXCHANGE"}:
            return "NSE"
        if normalized in {"B", "BOMBAY STOCK EXCHANGE"}:
            return "BSE"
        if normalized in {"X", "MULTIPLE", "ALL"}:
            return "BOTH"
        return normalized

    def _normalize_listing_status(self, value: str | None) -> str | None:
        """Normalize listing status values to a standard vocabulary."""
        if value is None:
            return None
        normalized = str(value).strip().lower()
        if normalized in {"active", "active listing", "listed"}:
            return "Active"
        if normalized in {"delisted", "inactive", "suspended"}:
            return "Delisted"
        return str(value).strip()