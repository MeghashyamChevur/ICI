"""Parsing utilities for company master payloads."""

from __future__ import annotations

from typing import Any

from ...models.company import Company


class CompanyMasterParser:
    """Convert raw company master payloads into Company model instances."""

    def parse(self, payload: Any) -> list[Company]:
        """Parse the payload into a list of Company objects."""

        if not isinstance(payload, dict):
            return []

        records = payload.get("records", [])
        if not isinstance(records, list):
            return []

        companies: list[Company] = []

        for record in records:
            if not isinstance(record, dict):
                continue

            companies.append(self._parse_record(record))

        return companies

    def _parse_record(self, record: dict[str, Any]) -> Company:
        """Convert a single raw record mapping to a Company instance."""
        return Company(
            symbol=str(record.get("symbol", "")).strip().upper(),
            company_name=str(record.get("company_name") or record.get("companyName") or "").strip(),
            isin=record.get("isin"),
            nse_code=record.get("nse_code"),
            bse_code=record.get("bse_code"),
            sector=record.get("sector"),
            industry=record.get("industry"),
            exchange=record.get("exchange"),
            listing_status=record.get("listing_status"),
            market_cap=self._coerce_float(record.get("market_cap")),
            market_cap_category=record.get("market_cap_category"),
            listing_date=record.get("listing_date"),
            face_value=self._coerce_float(record.get("face_value")),
            website=record.get("website"),
            headquarters=record.get("headquarters"),
            business_description=record.get("business_description"),
        )

    def _coerce_float(self, value: Any) -> float | None:
        """Coerce a value to a float when possible."""
        if value in (None, ""):
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None