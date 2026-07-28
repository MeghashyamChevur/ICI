"""Validation utilities for company financial records."""

from __future__ import annotations

from ...models.company_financials import CompanyFinancials


class CompanyFinancialsValidator:
    """Validate CompanyFinancials domain objects."""

    def validate(self, item: CompanyFinancials) -> None:
        """Validate a single financial record."""
        if not item.symbol:
            raise ValueError("Company symbol is required.")

        numeric_fields = {
            "revenue": item.revenue,
            "net_profit": item.net_profit,
            "eps": item.eps,
            "book_value": item.book_value,
            "roe": item.roe,
            "roce": item.roce,
            "debt_to_equity": item.debt_to_equity,
            "operating_margin": item.operating_margin,
            "promoter_holding": item.promoter_holding,
            "dividend_yield": item.dividend_yield,
        }

        for field_name, value in numeric_fields.items():
            if value is not None and not isinstance(value, (int, float)):
                raise ValueError(f"{field_name} must be numeric.")