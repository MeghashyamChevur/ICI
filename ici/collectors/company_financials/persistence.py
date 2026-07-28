"""CSV persistence utilities for company financials collector output."""

from __future__ import annotations

import csv
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from ...models.company_financials import CompanyFinancials


class CompanyFinancialsPersistence:
    """Persist CompanyFinancials model instances to CSV and load them back."""

    _FIELDNAMES = [
        "symbol",
        "revenue",
        "net_profit",
        "eps",
        "book_value",
        "roe",
        "roce",
        "debt_to_equity",
        "operating_margin",
        "promoter_holding",
        "dividend_yield",
    ]

    def __init__(self, output_path: str | Path | None = None) -> None:
        """Initialize persistence with an optional output path."""
        self.output_path = (
            Path(output_path)
            if output_path is not None
            else Path("reports/company_financials.csv")
        )

    def save(self, items: Sequence[CompanyFinancials]) -> Path:
        """Write the provided financial records to CSV and return the written path."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with self.output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=self._FIELDNAMES)
            writer.writeheader()

            for item in items:
                writer.writerow(self._serialize_financials(item))

        return self.output_path

    def load(self) -> list[CompanyFinancials]:
        """Load financial records from CSV and return them as CompanyFinancials objects."""
        if not self.output_path.exists():
            return []

        with self.output_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, fieldnames=self._FIELDNAMES)
            rows = list(reader)

        financials: list[CompanyFinancials] = []

        for row in rows:
            if not any((value or "").strip() for value in row.values()):
                continue

            if (
                row.get("symbol") == "symbol"
                and row.get("revenue") == "revenue"
            ):
                continue

            financials.append(self._deserialize_financials(row))

        return financials

    def _serialize_financials(
        self,
        item: CompanyFinancials,
    ) -> dict[str, Any]:
        """Convert a CompanyFinancials object into a CSV-friendly dictionary."""
        return {
            "symbol": item.symbol,
            "revenue": "" if item.revenue is None else str(item.revenue),
            "net_profit": "" if item.net_profit is None else str(item.net_profit),
            "eps": "" if item.eps is None else str(item.eps),
            "book_value": "" if item.book_value is None else str(item.book_value),
            "roe": "" if item.roe is None else str(item.roe),
            "roce": "" if item.roce is None else str(item.roce),
            "debt_to_equity": "" if item.debt_to_equity is None else str(item.debt_to_equity),
            "operating_margin": "" if item.operating_margin is None else str(item.operating_margin),
            "promoter_holding": "" if item.promoter_holding is None else str(item.promoter_holding),
            "dividend_yield": "" if item.dividend_yield is None else str(item.dividend_yield),
        }

    def _deserialize_financials(
        self,
        row: dict[str, Any],
    ) -> CompanyFinancials:
        """Convert a CSV row dictionary into a CompanyFinancials object."""
        return CompanyFinancials(
            symbol=str(row.get("symbol") or ""),
            revenue=self._to_float(row.get("revenue")),
            net_profit=self._to_float(row.get("net_profit")),
            eps=self._to_float(row.get("eps")),
            book_value=self._to_float(row.get("book_value")),
            roe=self._to_float(row.get("roe")),
            roce=self._to_float(row.get("roce")),
            debt_to_equity=self._to_float(row.get("debt_to_equity")),
            operating_margin=self._to_float(row.get("operating_margin")),
            promoter_holding=self._to_float(row.get("promoter_holding")),
            dividend_yield=self._to_float(row.get("dividend_yield")),
        )

    @staticmethod
    def _to_float(value: Any) -> float | None:
        """Convert a CSV value to float."""
        if value in (None, ""):
            return None

        return float(value)