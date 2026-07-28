"""Normalization utilities for company financial records."""

from __future__ import annotations

from ...models.company_financials import CompanyFinancials


class CompanyFinancialsNormalizer:
    """Normalize CompanyFinancials domain objects."""

    def normalize_many(
        self,
        financials: list[CompanyFinancials],
    ) -> list[CompanyFinancials]:
        """Normalize a collection of financial records."""
        return [self.normalize(item) for item in financials]

    def normalize(self, item: CompanyFinancials) -> CompanyFinancials:
        """Normalize a single financial record."""
        return CompanyFinancials(
            symbol=self._normalize_symbol(item.symbol),
            revenue=item.revenue,
            net_profit=item.net_profit,
            eps=item.eps,
            book_value=item.book_value,
            roe=item.roe,
            roce=item.roce,
            debt_to_equity=item.debt_to_equity,
            operating_margin=item.operating_margin,
            promoter_holding=item.promoter_holding,
            dividend_yield=item.dividend_yield,
        )

    def _normalize_symbol(self, value: str) -> str:
        """Normalize trading symbols."""
        return str(value).strip().upper()