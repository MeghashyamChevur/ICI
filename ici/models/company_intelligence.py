from dataclasses import dataclass

from .company import Company
from .company_financials import CompanyFinancials


@dataclass(slots=True)
class CompanyIntelligence:
    """
    Represents the complete intelligence available for a company.
    """

    company: Company
    financials: CompanyFinancials