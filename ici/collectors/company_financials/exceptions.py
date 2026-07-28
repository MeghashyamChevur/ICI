"""Exceptions for the company financials collector."""


class CompanyFinancialsError(Exception):
    """Base exception for company financials collection."""


class CompanyFinancialsDownloadError(CompanyFinancialsError):
    """Raised when financial data cannot be downloaded."""


class CompanyFinancialsDecodeError(CompanyFinancialsError):
    """Raised when financial data cannot be decoded."""