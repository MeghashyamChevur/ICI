"""Abstract base class for collectors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseCollector(ABC, Generic[T]):
    """Base interface for all collectors."""

    name: str = "base"

    @abstractmethod
    def collect(self) -> list[T]:
        """Collect and return a list of domain objects."""

    @abstractmethod
    def validate(self, item: T) -> bool:
        """Validate a single collected item."""

    def collect_validated(self) -> list[T]:
        """Collect items and return only the validated ones."""
        collected = self.collect()
        return [item for item in collected if self.validate(item)]
