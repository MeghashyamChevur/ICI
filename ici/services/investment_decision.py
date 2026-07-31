
"""Investment decision service."""

from __future__ import annotations

from ..constants.investment import (
    FINANCIAL_STRENGTH_WEIGHT,
    QUALITY_WEIGHT,
    SHAREHOLDER_RETURN_WEIGHT,
    TARGET_DEBT_TO_EQUITY,
    TARGET_DIVIDEND_YIELD,
    TARGET_OPERATING_MARGIN,
    TARGET_PROMOTER_HOLDING,
    TARGET_ROCE,
    TARGET_ROE,
)
from ..models import (
    CompanyIntelligence,
    InvestmentResult,
)
from .investment_summary import (
    InvestmentSummaryService,
)


class InvestmentDecisionService:
    """Calculates the final investment decision for a company."""

    def __init__(
        self,
    ) -> None:
        """Initialize the investment decision service."""

        self._summary_service = (
            InvestmentSummaryService()
        )

    def evaluate(
        self,
        intelligence: CompanyIntelligence,
    ) -> InvestmentResult:
        """Evaluate a company and return an investment result."""

        quality_score = (
            self._calculate_quality_score(
                intelligence,
            )
        )

        financial_strength_score = (
            self._calculate_financial_strength_score(
                intelligence,
            )
        )

        shareholder_return_score = (
            self._calculate_shareholder_return_score(
                intelligence,
            )
        )

        overall_score = (
            quality_score
            * QUALITY_WEIGHT
            + financial_strength_score
            * FINANCIAL_STRENGTH_WEIGHT
            + shareholder_return_score
            * SHAREHOLDER_RETURN_WEIGHT
        )

        grade = self._grade(
            overall_score,
        )

        recommendation = (
            self._recommendation(
                overall_score,
            )
        )

        confidence = (
            self._confidence(
                intelligence,
            )
        )

        strengths = (
            self._build_strengths(
                intelligence,
            )
        )

        weaknesses = (
            self._build_weaknesses(
                intelligence,
            )
        )

        summary = (
            self._summary_service.build(
                intelligence,
            )
        )

        return InvestmentResult(
            overall_score=round(
                overall_score,
                2,
            ),
            quality_score=round(
                quality_score,
                2,
            ),
            financial_strength_score=round(
                financial_strength_score,
                2,
            ),
            shareholder_return_score=round(
                shareholder_return_score,
                2,
            ),
            grade=grade,
            summary=summary,
            recommendation=recommendation,
            confidence=confidence,
            strengths=strengths,
            weaknesses=weaknesses,
        )
    def _calculate_quality_score(
        self,
        intelligence: CompanyIntelligence,
    ) -> float:
        """Calculate business quality score."""

        financials = intelligence.financials

        roe_score = self._normalize_positive(
            financials.roe,
            TARGET_ROE,
        )

        roce_score = self._normalize_positive(
            financials.roce,
            TARGET_ROCE,
        )

        operating_margin_score = (
            self._normalize_positive(
                financials.operating_margin,
                TARGET_OPERATING_MARGIN,
            )
        )

        return (
            roe_score
            + roce_score
            + operating_margin_score
        ) / 3

    def _calculate_financial_strength_score(
        self,
        intelligence: CompanyIntelligence,
    ) -> float:
        """Calculate financial strength score."""

        financials = intelligence.financials

        debt_score = self._normalize_inverse(
            financials.debt_to_equity,
            TARGET_DEBT_TO_EQUITY,
        )

        promoter_score = self._normalize_positive(
            financials.promoter_holding,
            TARGET_PROMOTER_HOLDING,
        )

        return (
            debt_score
            + promoter_score
        ) / 2

    def _calculate_shareholder_return_score(
        self,
        intelligence: CompanyIntelligence,
    ) -> float:
        """Calculate shareholder return score."""

        return self._normalize_positive(
            intelligence.financials.dividend_yield,
            TARGET_DIVIDEND_YIELD,
        )

    def _normalize_positive(
        self,
        value: float | None,
        target: float,
    ) -> float:
        """
        Normalize a metric where higher values are better.

        A company receives full marks once it reaches
        the target threshold.
        """

        if value is None:
            return 0.0

        return min(
            value / target,
            1.0,
        ) * 100

    def _normalize_inverse(
        self,
        value: float | None,
        target: float,
    ) -> float:
        """
        Normalize a metric where lower values are better.

        A company receives full marks when debt is zero
        and zero marks once it reaches the target threshold.
        """

        if value is None:
            return 0.0

        if value <= 0:
            return 100.0

        if value >= target:
            return 0.0

        return (
            (target - value)
            / target
        ) * 100
    def _build_strengths(
        self,
        intelligence: CompanyIntelligence,
    ) -> list[str]:
        """Build investment strengths."""

        financials = intelligence.financials

        strengths: list[str] = []

        if (
            financials.roe is not None
            and financials.roe >= TARGET_ROE
        ):
            strengths.append(
                f"ROE of {financials.roe:.2f}% exceeds "
                f"the target of {TARGET_ROE:.0f}%."
            )

        if (
            financials.roce is not None
            and financials.roce >= TARGET_ROCE
        ):
            strengths.append(
                f"ROCE of {financials.roce:.2f}% exceeds "
                f"the target of {TARGET_ROCE:.0f}%."
            )

        if (
            financials.operating_margin is not None
            and financials.operating_margin
            >= TARGET_OPERATING_MARGIN
        ):
            strengths.append(
                f"Operating Margin of "
                f"{financials.operating_margin:.2f}% "
                f"exceeds the target of "
                f"{TARGET_OPERATING_MARGIN:.0f}%."
            )

        if (
            financials.debt_to_equity is not None
        ):
            if financials.debt_to_equity <= 0:
                strengths.append(
                    "The company is debt free."
                )
            elif (
                financials.debt_to_equity
                < TARGET_DEBT_TO_EQUITY
            ):
                strengths.append(
                    f"Debt-to-Equity of "
                    f"{financials.debt_to_equity:.2f} "
                    f"is within the target limit of "
                    f"{TARGET_DEBT_TO_EQUITY:.2f}."
                )

        if (
            financials.promoter_holding is not None
            and financials.promoter_holding
            >= TARGET_PROMOTER_HOLDING
        ):
            strengths.append(
                f"Promoter Holding of "
                f"{financials.promoter_holding:.2f}% "
                f"exceeds the target of "
                f"{TARGET_PROMOTER_HOLDING:.0f}%."
            )

        if (
            financials.dividend_yield is not None
            and financials.dividend_yield
            >= TARGET_DIVIDEND_YIELD
        ):
            strengths.append(
                f"Dividend Yield of "
                f"{financials.dividend_yield:.2f}% "
                f"meets the target of "
                f"{TARGET_DIVIDEND_YIELD:.0f}%."
            )

        return strengths

    def _build_weaknesses(
        self,
        intelligence: CompanyIntelligence,
    ) -> list[str]:
        """Build investment weaknesses."""

        financials = intelligence.financials

        weaknesses: list[str] = []

        if (
            financials.roe is not None
            and financials.roe < TARGET_ROE
        ):
            weaknesses.append(
                f"ROE of {financials.roe:.2f}% "
                f"is below the target of "
                f"{TARGET_ROE:.0f}%."
            )

        if (
            financials.roce is not None
            and financials.roce < TARGET_ROCE
        ):
            weaknesses.append(
                f"ROCE of {financials.roce:.2f}% "
                f"is below the target of "
                f"{TARGET_ROCE:.0f}%."
            )

        if (
            financials.operating_margin is not None
            and financials.operating_margin
            < TARGET_OPERATING_MARGIN
        ):
            weaknesses.append(
                f"Operating Margin of "
                f"{financials.operating_margin:.2f}% "
                f"is below the target of "
                f"{TARGET_OPERATING_MARGIN:.0f}%."
            )
        if (
            financials.debt_to_equity is not None
            and financials.debt_to_equity
            >= TARGET_DEBT_TO_EQUITY
        ):
            weaknesses.append(
                f"Debt-to-Equity of "
                f"{financials.debt_to_equity:.2f} "
                f"exceeds the target limit of "
                f"{TARGET_DEBT_TO_EQUITY:.2f}."
            )

        if (
            financials.promoter_holding is not None
            and financials.promoter_holding
            < TARGET_PROMOTER_HOLDING
        ):
            weaknesses.append(
                f"Promoter Holding of "
                f"{financials.promoter_holding:.2f}% "
                f"is below the target of "
                f"{TARGET_PROMOTER_HOLDING:.0f}%."
            )

        if (
            financials.dividend_yield is not None
            and financials.dividend_yield
            < TARGET_DIVIDEND_YIELD
        ):
            weaknesses.append(
                f"Dividend Yield of "
                f"{financials.dividend_yield:.2f}% "
                f"is below the target of "
                f"{TARGET_DIVIDEND_YIELD:.0f}%."
            )

        return weaknesses

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
