"""Validation framework for collector output."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class ValidationResult(Generic[T]):
    """Represents the outcome of validating an item."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    item: T | None = None


class BaseValidator(Generic[T]):
    """Base validator interface with placeholder methods."""

    def validate(self, item: T) -> ValidationResult[T]:
        """Validate an item and return a result object."""
        return ValidationResult(is_valid=True, item=item)

    def validate_many(self, items: list[T]) -> list[ValidationResult[T]]:
        """Validate a collection of items."""
        return [self.validate(item) for item in items]
