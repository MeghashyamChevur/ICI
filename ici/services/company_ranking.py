"""Company ranking service."""

from __future__ import annotations

from ici.models import (
    CompanyIntelligence,
    RankingResult,
)


class CompanyRankingService:
    """Calculate ranking scores for screened companies."""

    ROE_WEIGHT = 0.25
    ROCE_WEIGHT = 0.25
    OPERATING_MARGIN_WEIGHT = 0.20
    DEBT_TO_EQUITY_WEIGHT = 0.15
    PROMOTER_HOLDING_WEIGHT = 0.15

    MAX_ROE = 50.0
    MAX_ROCE = 50.0
    MAX_OPERATING_MARGIN = 40.0
    MAX_PROMOTER_HOLDING = 75.0
    MAX_DEBT_TO_EQUITY = 0.50

    def calculate_score(
        self,
        intelligence: CompanyIntelligence,
    ) -> float:
        """Calculate weighted score for a company."""

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

        promoter_holding_score = self._normalize_positive(
            financials.promoter_holding,
            self.MAX_PROMOTER_HOLDING,
        )

        debt_to_equity_score = self._normalize_inverse(
            financials.debt_to_equity,
            self.MAX_DEBT_TO_EQUITY,
        )

        score = (
            roe_score * self.ROE_WEIGHT
            + roce_score * self.ROCE_WEIGHT
            + operating_margin_score
            * self.OPERATING_MARGIN_WEIGHT
            + debt_to_equity_score
            * self.DEBT_TO_EQUITY_WEIGHT
            + promoter_holding_score
            * self.PROMOTER_HOLDING_WEIGHT
        )

        return round(score, 2)

    def create_ranking(
        self,
        rank: int,
        intelligence: CompanyIntelligence,
    ) -> RankingResult:
        """Create ranking information for a company."""

        score = self.calculate_score(intelligence)

        return RankingResult(
            rank=rank,
            score=score,
            grade=self._grade(score),
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
        """Assign a grade based on the score."""

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