"""Collector for screening companies."""

from __future__ import annotations

import json
from pathlib import Path

from ici.models import (
    Company,
    CompanyFinancials,
    CompanyIntelligence,
)
from ici.persistence.company_screening_persistence import (
    CompanyScreeningPersistence,
)
from ici.services import CompanyScreeningService


class CompanyScreeningCollector:
    """Screen companies using company intelligence data."""

    def __init__(
        self,
        company_intelligence_path: Path,
        output_path: Path,
    ) -> None:
        self.company_intelligence_path = company_intelligence_path
        self.output_path = output_path

        self.persistence = CompanyScreeningPersistence()
        self.service = CompanyScreeningService()

    def collect(self) -> list[dict[str, object]]:
        """Screen and persist qualified companies."""

        intelligence = self._load_company_intelligence()

        qualified: list[dict[str, object]] = []

        for company in intelligence:
            screening = self.service.evaluate(company)

            if not screening.qualified:
                continue

            qualified.append(
                {
                    "company": company.company,
                    "financials": company.financials,
                    "screening": screening,
                }
            )

        self.persistence.save(
            qualified,
            self.output_path,
        )

        return qualified

    def _load_company_intelligence(
        self,
    ) -> list[CompanyIntelligence]:
        """Load company intelligence records from JSON."""

        intelligence: list[CompanyIntelligence] = []

        with self.company_intelligence_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        for record in data:
            company = Company(
                symbol=record["company"]["symbol"],
                company_name=record["company"]["company_name"],
                isin=record["company"].get("isin"),
                nse_code=record["company"].get("nse_code"),
                bse_code=record["company"].get("bse_code"),
                sector=record["company"].get("sector"),
                industry=record["company"].get("industry"),
                exchange=record["company"].get("exchange"),
                listing_status=record["company"].get("listing_status"),
                market_cap=record["company"].get("market_cap"),
                market_cap_category=record["company"].get(
                    "market_cap_category"
                ),
                listing_date=record["company"].get("listing_date"),
                face_value=record["company"].get("face_value"),
                website=record["company"].get("website"),
                headquarters=record["company"].get("headquarters"),
                business_description=record["company"].get(
                    "business_description"
                ),
            )

            financials = CompanyFinancials(
                symbol=record["financials"]["symbol"],
                revenue=record["financials"].get("revenue"),
                net_profit=record["financials"].get("net_profit"),
                eps=record["financials"].get("eps"),
                book_value=record["financials"].get("book_value"),
                roe=record["financials"].get("roe"),
                roce=record["financials"].get("roce"),
                debt_to_equity=record["financials"].get(
                    "debt_to_equity"
                ),
                operating_margin=record["financials"].get(
                    "operating_margin"
                ),
                promoter_holding=record["financials"].get(
                    "promoter_holding"
                ),
                dividend_yield=record["financials"].get(
                    "dividend_yield"
                ),
            )

            intelligence.append(
                CompanyIntelligence(
                    company=company,
                    financials=financials,
                )
            )

        return intelligence