"""CSV persistence utilities for company master collector output."""

from __future__ import annotations

import csv
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from ...models.company import Company


class CompanyMasterPersistence:
    """Persist Company model instances to CSV and load them back."""

    _FIELDNAMES = [
        "symbol",
        "company_name",
        "isin",
        "nse_code",
        "bse_code",
        "sector",
        "industry",
        "exchange",
        "listing_status",
        "market_cap",
        "market_cap_category",
        "listing_date",
        "face_value",
        "website",
        "headquarters",
        "business_description",
    ]

    def __init__(self, output_path: str | Path | None = None) -> None:
        """Initialize persistence with an optional output path."""
        self.output_path = Path(output_path) if output_path is not None else Path("reports/company_master.csv")

    def save(self, items: Sequence[Company]) -> Path:
        """Write the provided companies to CSV and return the written path."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with self.output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=self._FIELDNAMES)
            writer.writeheader()

            for item in items:
                writer.writerow(self._serialize_company(item))

        return self.output_path

    def load(self) -> list[Company]:
        """Load companies from CSV and return them as Company objects."""
        if not self.output_path.exists():
            return []

        with self.output_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, fieldnames=self._FIELDNAMES)
            rows = list(reader)

        companies: list[Company] = []

        for row in rows:
            if not any((value or "").strip() for value in row.values()):
                continue

            if row.get("symbol") == "symbol" and row.get("company_name") == "company_name":
                continue

            companies.append(self._deserialize_company(row))

        return companies

    def _serialize_company(self, item: Company) -> dict[str, Any]:
        """Convert a Company object into a CSV-friendly dictionary."""
        return {
            "symbol": item.symbol,
            "company_name": item.company_name,
            "isin": item.isin,
            "nse_code": item.nse_code,
            "bse_code": item.bse_code,
            "sector": item.sector,
            "industry": item.industry,
            "exchange": item.exchange,
            "listing_status": item.listing_status,
            "market_cap": "" if item.market_cap is None else str(item.market_cap),
            "market_cap_category": item.market_cap_category,
            "listing_date": item.listing_date,
            "face_value": "" if item.face_value is None else str(item.face_value),
            "website": item.website,
            "headquarters": item.headquarters,
            "business_description": item.business_description,
        }

    def _deserialize_company(self, row: dict[str, Any]) -> Company:
        """Convert a CSV row dictionary into a Company object."""
        market_cap_value = row.get("market_cap")
        market_cap = None if market_cap_value in (None, "") else float(market_cap_value)

        face_value_value = row.get("face_value")
        face_value = None if face_value_value in (None, "") else float(face_value_value)

        return Company(
            symbol=str(row.get("symbol") or ""),
            company_name=str(row.get("company_name") or ""),
            isin=row.get("isin") or None,
            nse_code=row.get("nse_code") or None,
            bse_code=row.get("bse_code") or None,
            sector=row.get("sector") or None,
            industry=row.get("industry") or None,
            exchange=row.get("exchange") or None,
            listing_status=row.get("listing_status") or None,
            market_cap=market_cap,
            market_cap_category=row.get("market_cap_category") or None,
            listing_date=row.get("listing_date") or None,
            face_value=face_value,
            website=row.get("website") or None,
            headquarters=row.get("headquarters") or None,
            business_description=row.get("business_description") or None,
        )