"""Company screening service."""

from __future__ import annotations

from ici.models import CompanyIntelligence, ScreeningResult


class CompanyScreeningService:
    """Apply screening rules to company intelligence."""

    MIN_ROE = 15.0
    MIN_ROCE = 15.0
    MAX_DEBT_TO_EQUITY = 0.50
    MIN_OPERATING_MARGIN = 15.0
    MIN_PROMOTER_HOLDING = 50.0

    def evaluate(
        self,
        intelligence: CompanyIntelligence,
    ) -> ScreeningResult:
        """Evaluate all screening rules for a company."""

        financials = intelligence.financials

        roe = (
            financials.roe is not None
            and financials.roe >= self.MIN_ROE
        )

        roce = (
            financials.roce is not None
            and financials.roce >= self.MIN_ROCE
        )

        debt_to_equity = (
            financials.debt_to_equity is not None
            and financials.debt_to_equity <= self.MAX_DEBT_TO_EQUITY
        )

        operating_margin = (
            financials.operating_margin is not None
            and financials.operating_margin >= self.MIN_OPERATING_MARGIN
        )

        promoter_holding = (
            financials.promoter_holding is not None
            and financials.promoter_holding >= self.MIN_PROMOTER_HOLDING
        )

        checks = [
            roe,
            roce,
            debt_to_equity,
            operating_margin,
            promoter_holding,
        ]

        passed_rules = sum(checks)
        total_rules = len(checks)

        return ScreeningResult(
            qualified=passed_rules == total_rules,
            score=passed_rules,
            total_rules=total_rules,
            passed_rules=passed_rules,
            roe=roe,
            roce=roce,
            debt_to_equity=debt_to_equity,
            operating_margin=operating_margin,
            promoter_holding=promoter_holding,
        )

    def is_qualified(
        self,
        intelligence: CompanyIntelligence,
    ) -> bool:
        """Return True if the company satisfies all screening rules."""

        return self.evaluate(intelligence).qualified