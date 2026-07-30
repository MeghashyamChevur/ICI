"""Ranking result model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RankingResult:
    """Represents a company's ranking."""

    rank: int
    score: float
    grade: str

    def to_dict(self) -> dict[str, object]:
        """Convert the ranking result to a dictionary."""

        return {
            "rank": self.rank,
            "score": round(self.score, 2),
            "grade": self.grade,
        }