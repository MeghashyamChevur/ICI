from ici.models import (
    Company,
    CompanyFinancials,
    CompanyIntelligence,
)


class CompanyIntelligenceBuilder:
    """
    Builds CompanyIntelligence objects.
    """

    def build(
        self,
        company: Company,
        financials: CompanyFinancials,
    ) -> CompanyIntelligence:
        """
        Combine company profile and financial data.
        """
        return CompanyIntelligence(
            company=company,
            financials=financials,
        )