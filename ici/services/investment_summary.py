"""Investment summary service."""

from __future__ import annotations

from ..constants.investment import (
    TARGET_DEBT_TO_EQUITY,
    TARGET_DIVIDEND_YIELD,
    TARGET_OPERATING_MARGIN,
    TARGET_PROMOTER_HOLDING,
    TARGET_ROCE,
    TARGET_ROE,
)
from ..models import CompanyIntelligence


class InvestmentSummaryService:
    """Builds an analyst-style investment summary."""

    def build(
        self,
        intelligence: CompanyIntelligence,
    ) -> str:
        """Build an investment summary."""

        sections: list[str] = []

        business = self._business_quality(intelligence)
        if business:
            sections.append(business)

        financial = self._financial_strength(intelligence)
        if financial:
            sections.append(financial)

        ownership = self._ownership(
            intelligence,
        )
        if ownership:
            sections.append(
                ownership,
            )

        dividend = self._dividend(
            intelligence,
        )
        if dividend:
            sections.append(
                dividend,
            )

        overall = self._overall_conclusion(
            intelligence,
        )
        if overall:
            sections.append(
                overall,
            )

        return " ".join(
            sections,
        )
        

    def _business_quality(
        self,
        intelligence: CompanyIntelligence,
    ) -> str:
        """Summarize business quality."""

        financials = intelligence.financials

        metrics = [
            financials.roe,
            financials.roce,
            financials.operating_margin,
        ]

        achieved = 0

        if (
            financials.roe is not None
            and financials.roe >= TARGET_ROE
        ):
            achieved += 1

        if (
            financials.roce is not None
            and financials.roce >= TARGET_ROCE
        ):
            achieved += 1

        if (
            financials.operating_margin is not None
            and financials.operating_margin
            >= TARGET_OPERATING_MARGIN
        ):
            achieved += 1

        available = sum(metric is not None for metric in metrics)

        if available == 0:
            return ""

        if achieved == 3:
            return (
                "The company demonstrates outstanding profitability with "
                "strong ROE, ROCE and operating margin."
            )

        if achieved == 2:
            return (
                "The company demonstrates healthy profitability, although "
                "some return metrics remain below the preferred targets."
            )

        if achieved == 1:
            return (
                "The company has mixed profitability, with only one of the "
                "key profitability metrics meeting the preferred target."
            )

        return (
            "The company's profitability metrics remain below the preferred "
            "targets, reducing overall investment attractiveness."
        )

    def _financial_strength(
        self,
        intelligence: CompanyIntelligence,
    ) -> str:
        """Summarize financial strength."""

        debt = intelligence.financials.debt_to_equity

        if debt is None:
            return ""

        if debt <= 0:
            return "The company is debt free."

        if debt < TARGET_DEBT_TO_EQUITY / 2:
            return "The company maintains a very conservative debt position."

        if debt < TARGET_DEBT_TO_EQUITY:
            return "Debt levels remain within the preferred limit."

        return "Debt levels are higher than the preferred limit."

    def _ownership(
        self,
        intelligence: CompanyIntelligence,
    ) -> str:
        """Summarize promoter ownership."""

        promoter = intelligence.financials.promoter_holding

        if promoter is None:
            return ""

        if promoter >= TARGET_PROMOTER_HOLDING:
            return "Promoter ownership remains strong."

        if promoter >= 40:
            return (
                "Promoter ownership is moderate but below the preferred "
                "level."
            )

        return "Promoter ownership is relatively low."

    def _dividend(
        self,
        intelligence: CompanyIntelligence,
    ) -> str:
        """Summarize dividend profile."""

        dividend = intelligence.financials.dividend_yield

        if dividend is None:
            return ""

        if dividend >= TARGET_DIVIDEND_YIELD:
            return "Dividend yield meets the preferred target."

        if dividend >= 1:
            return "Dividend yield is modest."

        return (
            "Dividend yield is low, indicating the company prioritizes "
            "reinvestment over shareholder payouts."
        )
    def _overall_conclusion(
        self,
        intelligence: CompanyIntelligence,
    ) -> str:
        """Build the overall analyst conclusion."""

        financials = intelligence.financials

        achieved = 0

        if (
            financials.roe is not None
            and financials.roe >= TARGET_ROE
        ):
            achieved += 1

        if (
            financials.roce is not None
            and financials.roce >= TARGET_ROCE
        ):
            achieved += 1

        if (
            financials.operating_margin is not None
            and financials.operating_margin
            >= TARGET_OPERATING_MARGIN
        ):
            achieved += 1

        if (
            financials.promoter_holding is not None
            and financials.promoter_holding
            >= TARGET_PROMOTER_HOLDING
        ):
            achieved += 1

        if (
            financials.debt_to_equity is not None
            and financials.debt_to_equity
            < TARGET_DEBT_TO_EQUITY
        ):
            achieved += 1

        if achieved >= 5:
            return (
                "Overall, the company demonstrates excellent financial "
                "quality and appears suitable for long-term investors."
            )

        if achieved >= 3:
            return (
                "Overall, the company meets most quality benchmarks and "
                "appears suitable for long-term monitoring or gradual "
                "accumulation."
            )

        return (
            "Overall, the company falls short of several preferred "
            "investment benchmarks and should be monitored for further "
            "improvement before significant investment."
        )