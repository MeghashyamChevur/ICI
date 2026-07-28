"""Registry for collector implementations."""

from __future__ import annotations

from typing import Dict, Type

from .base import BaseCollector
from .company_master import CompanyMasterCollector
from .company_financials.collector import CompanyFinancialsCollector


class CollectorRegistry:
    """Simple registry that stores collectors by name."""

    def __init__(self) -> None:
        self._collectors: Dict[str, Type[BaseCollector]] = {}

    def register(self, collector_cls: Type[BaseCollector]) -> None:
        """Register a collector implementation."""
        self._collectors[collector_cls.name] = collector_cls

    def get(self, name: str) -> Type[BaseCollector]:
        """Retrieve a collector class by name."""
        if name not in self._collectors:
            raise KeyError(f"Collector '{name}' is not registered")
        return self._collectors[name]

    def list(self) -> list[str]:
        """Return all registered collector names."""
        return sorted(self._collectors)


_registry = CollectorRegistry()
_registry.register(CompanyMasterCollector)
_registry.register(CompanyFinancialsCollector)


def get_registry() -> CollectorRegistry:
    """Return the module-level registry instance."""
    return _registry
