"""Collector for building company intelligence reports."""

from __future__ import annotations

import csv
from pathlib import Path

from ici.models import (
    Company,
    CompanyFinancials,
    CompanyIntelligence,
)
from ici.persistence import CompanyIntelligencePersistence
from ici.services import CompanyIntelligenceBuilder


class CompanyIntelligenceCollector:
    """Build company intelligence by combining company and financial data."""

    def __init__(
        self,
        company_master_path: Path,
        company_financials_path: Path,
        output_path: Path,
    ) -> None:
        self.company_master_path = company_master_path
        self.company_financials_path = company_financials_path
        self.output_path = output_path

        self.persistence = CompanyIntelligencePersistence()
        self.builder = CompanyIntelligenceBuilder()

    def collect(self) -> list[CompanyIntelligence]:
        """Build and persist company intelligence."""

        companies = self._load_companies()
        financials = self._load_financials()

        financial_lookup = {
            financial.symbol: financial
            for financial in financials
        }

        intelligence: list[CompanyIntelligence] = []

        for company in companies:
            financial = financial_lookup.get(company.symbol)

            if financial is None:
                continue

            intelligence.append(
                self.builder.build(
                    company,
                    financial,
                )
            )

        self.persistence.save(
            intelligence,
            self.output_path,
        )

        return intelligence

    def _load_companies(self) -> list[Company]:
        """Load company master records from CSV."""

        companies: list[Company] = []

        with self.company_master_path.open(
            mode="r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                companies.append(
                    Company(
                        symbol=row["symbol"],
                        company_name=row["company_name"],
                        isin=row["isin"] or None,
                        nse_code=row["nse_code"] or None,
                        bse_code=row["bse_code"] or None,
                        sector=row["sector"] or None,
                        industry=row["industry"] or None,
                        exchange=row["exchange"] or None,
                        listing_status=row["listing_status"] or None,
                        market_cap=float(row["market_cap"])
                        if row["market_cap"]
                        else None,
                        market_cap_category=row["market_cap_category"] or None,
                        listing_date=row["listing_date"] or None,
                        face_value=float(row["face_value"])
                        if row["face_value"]
                        else None,
                        website=row["website"] or None,
                        headquarters=row["headquarters"] or None,
                        business_description=row["business_description"] or None,
                    )
                )

        return companies

    def _load_financials(self) -> list[CompanyFinancials]:
        """Load company financial records from CSV."""

        financials: list[CompanyFinancials] = []

        with self.company_financials_path.open(
            mode="r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                financials.append(
                    CompanyFinancials(
                        symbol=row["symbol"],
                        revenue=float(row["revenue"]) if row["revenue"] else None,
                        net_profit=float(row["net_profit"])
                        if row["net_profit"]
                        else None,
                        eps=float(row["eps"]) if row["eps"] else None,
                        book_value=float(row["book_value"])
                        if row["book_value"]
                        else None,
                        roe=float(row["roe"]) if row["roe"] else None,
                        roce=float(row["roce"]) if row["roce"] else None,
                        debt_to_equity=float(row["debt_to_equity"])
                        if row["debt_to_equity"]
                        else None,
                        operating_margin=float(row["operating_margin"])
                        if row["operating_margin"]
                        else None,
                        promoter_holding=float(row["promoter_holding"])
                        if row["promoter_holding"]
                        else None,
                        dividend_yield=float(row["dividend_yield"])
                        if row["dividend_yield"]
                        else None,
                    )
                )

        return financials