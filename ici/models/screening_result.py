"""Screening result model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ScreeningResult:
    """Represents the outcome of screening a company."""

    qualified: bool
    score: int
    total_rules: int
    passed_rules: int

    roe: bool
    roce: bool
    debt_to_equity: bool
    operating_margin: bool
    promoter_holding: bool

    def to_dict(self) -> dict[str, object]:
        """Return the screening result as a dictionary."""

        return {
            "qualified": self.qualified,
            "score": self.score,
            "total_rules": self.total_rules,
            "passed_rules": self.passed_rules,
            "checks": {
                "roe": self.roe,
                "roce": self.roce,
                "debt_to_equity": self.debt_to_equity,
                "operating_margin": self.operating_margin,
                "promoter_holding": self.promoter_holding,
            },
        }