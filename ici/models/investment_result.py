"""Investment result model."""

from dataclasses import dataclass


@dataclass(slots=True)
class InvestmentResult:
    """Represents the final investment evaluation for a company."""

    overall_score: float
    quality_score: float
    financial_strength_score: float
    shareholder_return_score: float
    grade: str
    recommendation: str
    confidence: str

    def to_dict(self) -> dict[str, object]:
        """Convert the investment result to a dictionary."""

        return {
            "overall_score": self.overall_score,
            "quality_score": self.quality_score,
            "financial_strength_score": self.financial_strength_score,
            "shareholder_return_score": self.shareholder_return_score,
            "grade": self.grade,
            "recommendation": self.recommendation,
            "confidence": self.confidence,
        }