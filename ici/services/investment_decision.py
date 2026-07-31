"""Investment decision service."""

from __future__ import annotations

from ..models import CompanyIntelligence, InvestmentResult


class InvestmentDecisionService:
    """Calculates the final investment decision for a company."""

    QUALITY_WEIGHT = 0.50
    FINANCIAL_STRENGTH_WEIGHT = 0.30
    SHAREHOLDER_RETURN_WEIGHT = 0.20

    MAX_ROE = 50.0
    MAX_ROCE = 50.0
    MAX_OPERATING_MARGIN = 40.0
    MAX_PROMOTER_HOLDING = 75.0
    MAX_DEBT_TO_EQUITY = 0.50
    MAX_DIVIDEND_YIELD = 5.0

    def evaluate(
        self,
        intelligence: CompanyIntelligence,
    ) -> InvestmentResult:
        """Evaluate a company and return an investment result."""

        quality_score = self._calculate_quality_score(intelligence)

        financial_strength_score = (
            self._calculate_financial_strength_score(
                intelligence
            )
        )

        shareholder_return_score = (
            self._calculate_shareholder_return_score(
                intelligence
            )
        )

        overall_score = (
            quality_score * self.QUALITY_WEIGHT
            + financial_strength_score
            * self.FINANCIAL_STRENGTH_WEIGHT
            + shareholder_return_score
            * self.SHAREHOLDER_RETURN_WEIGHT
        )

        grade = self._grade(overall_score)
        recommendation = self._recommendation(overall_score)
        confidence = self._confidence(intelligence)

        return InvestmentResult(
            overall_score=round(overall_score, 2),
            quality_score=round(quality_score, 2),
            financial_strength_score=round(
                financial_strength_score,
                2,
            ),
            shareholder_return_score=round(
                shareholder_return_score,
                2,
            ),
            grade=grade,
            recommendation=recommendation,
            confidence=confidence,
        )

    def _calculate_quality_score(
        self,
        intelligence: CompanyIntelligence,
    ) -> float:
        """Calculate business quality score."""

        financials = intelligence.financials

        roe_score = self._normalize_positive(
            financials.roe,
            self.MAX_ROE,
        )

        roce_score = self._normalize_positive(
            financials.roce,
            self.MAX_ROCE,
        )

        operating_margin_score = self._normalize_positive(
            financials.operating_margin,
            self.MAX_OPERATING_MARGIN,
        )

        score = (
            roe_score
            + roce_score
            + operating_margin_score
        ) / 3

        return score

    def _calculate_financial_strength_score(
        self,
        intelligence: CompanyIntelligence,
    ) -> float:
        """Calculate financial strength score."""

        financials = intelligence.financials

        debt_score = self._normalize_inverse(
            financials.debt_to_equity,
            self.MAX_DEBT_TO_EQUITY,
        )

        promoter_score = self._normalize_positive(
            financials.promoter_holding,
            self.MAX_PROMOTER_HOLDING,
        )

        score = (
            debt_score
            + promoter_score
        ) / 2

        return score

    def _calculate_shareholder_return_score(
        self,
        intelligence: CompanyIntelligence,
    ) -> float:
        """Calculate shareholder return score."""

        return self._normalize_positive(
            intelligence.financials.dividend_yield,
            self.MAX_DIVIDEND_YIELD,
        )

    def _normalize_positive(
        self,
        value: float | None,
        maximum: float,
    ) -> float:
        """Normalize a metric where higher values are better."""

        if value is None:
            return 0.0

        return min(value / maximum, 1.0) * 100

    def _normalize_inverse(
        self,
        value: float | None,
        maximum: float,
    ) -> float:
        """Normalize a metric where lower values are better."""

        if value is None:
            return 0.0

        if value >= maximum:
            return 0.0

        return ((maximum - value) / maximum) * 100

    def _grade(
        self,
        score: float,
    ) -> str:
        """Return investment grade."""

        if score >= 90:
            return "A+"

        if score >= 80:
            return "A"

        if score >= 70:
            return "B+"

        if score >= 60:
            return "B"

        if score >= 50:
            return "C"

        return "D"

    def _recommendation(
        self,
        score: float,
    ) -> str:
        """Return investment recommendation."""

        if score >= 90:
            return "Strong Buy"

        if score >= 80:
            return "Buy"

        if score >= 70:
            return "Accumulate"

        if score >= 60:
            return "Hold"

        return "Avoid"

    def _confidence(
        self,
        intelligence: CompanyIntelligence,
    ) -> str:
        """Return confidence level based on data completeness."""

        financials = intelligence.financials

        metrics = [
            financials.roe,
            financials.roce,
            financials.operating_margin,
            financials.debt_to_equity,
            financials.promoter_holding,
            financials.dividend_yield,
        ]

        available = sum(
            metric is not None
            for metric in metrics
        )

        if available == len(metrics):
            return "High"

        if available >= 4:
            return "Medium"

        return "Low"