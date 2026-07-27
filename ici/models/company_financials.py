"""Company financial metrics domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CompanyFinancials:
    """Financial metrics for a listed company."""

    symbol: str

    revenue: float | None = None
    net_profit: float | None = None
    eps: float | None = None
    book_value: float | None = None

    roe: float | None = None
    roce: float | None = None
    debt_to_equity: float | None = None
    operating_margin: float | None = None

    promoter_holding: float | None = None
    dividend_yield: float | None = None