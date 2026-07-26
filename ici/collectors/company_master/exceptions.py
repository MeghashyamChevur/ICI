"""Exceptions used by the company master collector package."""

from __future__ import annotations

from ...exceptions import CollectorError


class CompanyMasterCollectorError(CollectorError):
    """Base exception for company master collector failures."""


class CompanyMasterParseError(CompanyMasterCollectorError):
    """Raised when a company master payload cannot be parsed."""


class CompanyMasterPersistenceError(CompanyMasterCollectorError):
    """Raised when persistence fails."""


class CompanyMasterValidationError(CompanyMasterCollectorError):
    """Raised when a company master record fails validation."""


class CompanyMasterSourceDownloadError(CompanyMasterCollectorError):
    """Raised when the company master source download fails."""


class CompanyMasterSourceDecodeError(CompanyMasterCollectorError):
    """Raised when the company master payload cannot be decoded."""
