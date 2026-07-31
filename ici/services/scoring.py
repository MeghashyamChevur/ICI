"""Shared scoring utilities."""

from __future__ import annotations


class ScoringService:
    """Utility methods for calculating normalized scores."""

    @staticmethod
    def normalize_positive(
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

        return min(value / target, 1.0) * 100

    @staticmethod
    def normalize_inverse(
        value: float | None,
        target: float,
    ) -> float:
        """
        Normalize a metric where lower values are better.

        A company receives full marks when the metric
        is zero and zero marks once it reaches the
        target threshold.
        """

        if value is None:
            return 0.0

        if value <= 0:
            return 100.0

        if value >= target:
            return 0.0

        return ((target - value) / target) * 100