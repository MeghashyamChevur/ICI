"""Custom exceptions for the ICI package."""


class ICIError(Exception):
    """Base exception for ICI package errors."""


class CollectorError(ICIError):
    """Raised when a collector fails."""


class ValidationError(ICIError):
    """Raised when validation fails."""
