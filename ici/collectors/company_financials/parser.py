"""Parsing utilities for company financial payloads."""

from __future__ import annotations

from typing import Any

from ...models.company_financials import CompanyFinancials


class CompanyFinancialsParser:
    """Convert raw financial payloads into CompanyFinancials model instances."""

    def parse(self, payload: Any) -> list[CompanyFinancials]:
        """Parse the payload into CompanyFinancials objects."""
        if not isinstance(payload, dict):
            return []

        records = payload.get("records", [])
        if not isinstance(records, list):
            return []

        financials: list[CompanyFinancials] = []

        for record in records:
            if not isinstance(record, dict):
                continue

            financials.append(self._parse_record(record))

        return financials

    def _parse_record(self, record: dict[str, Any]) -> CompanyFinancials:
        """Convert a raw record into a CompanyFinancials instance."""
        return CompanyFinancials(
            symbol=str(record.get("symbol", "")).strip().upper(),
            revenue=self._coerce_float(record.get("revenue")),
            net_profit=self._coerce_float(record.get("net_profit")),
            eps=self._coerce_float(record.get("eps")),
            book_value=self._coerce_float(record.get("book_value")),
            roe=self._coerce_float(record.get("roe")),
            roce=self._coerce_float(record.get("roce")),
            debt_to_equity=self._coerce_float(record.get("debt_to_equity")),
            operating_margin=self._coerce_float(record.get("operating_margin")),
            promoter_holding=self._coerce_float(record.get("promoter_holding")),
            dividend_yield=self._coerce_float(record.get("dividend_yield")),
        )

    def _coerce_float(self, value: Any) -> float | None:
        """Convert a value to float when possible."""
        if value in (None, ""):
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None