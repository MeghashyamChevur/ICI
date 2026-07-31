"""Collector for investment decisions."""

from __future__ import annotations

import json
from pathlib import Path

from ici.models import (
    Company,
    CompanyFinancials,
    CompanyIntelligence,
)
from ici.persistence import (
    InvestmentDecisionPersistence,
)
from ici.services import InvestmentDecisionService


class InvestmentDecisionCollector:
    """Generate investment decisions for screened companies."""

    def __init__(
        self,
        screened_companies_path: Path,
        output_path: Path,
    ) -> None:
        self.screened_companies_path = (
            screened_companies_path
        )
        self.output_path = output_path

        self.persistence = (
            InvestmentDecisionPersistence()
        )
        self.service = (
            InvestmentDecisionService()
        )

    def collect(
        self,
    ) -> list[dict[str, object]]:
        """Generate investment decisions."""

        records = self._load_screened_companies()

        results: list[dict[str, object]] = []

        for record in records:
            intelligence = record["intelligence"]
            screening = record["screening"]

            investment = self.service.evaluate(
                intelligence,
            )

            results.append(
                {
                    "company": intelligence.company,
                    "financials": intelligence.financials,
                    "screening": screening,
                    "investment": investment,
                }
            )

        self.persistence.save(
            results,
            self.output_path,
        )

        return results

    def _load_screened_companies(
        self,
    ) -> list[dict[str, object]]:
        """Load screened companies from JSON."""

        records: list[dict[str, object]] = []

        with self.screened_companies_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        for record in data:
            company = Company(
                symbol=record["company"]["symbol"],
                company_name=record["company"][
                    "company_name"
                ],
                isin=record["company"].get("isin"),
                nse_code=record["company"].get(
                    "nse_code"
                ),
                bse_code=record["company"].get(
                    "bse_code"
                ),
                sector=record["company"].get(
                    "sector"
                ),
                industry=record["company"].get(
                    "industry"
                ),
                exchange=record["company"].get(
                    "exchange"
                ),
                listing_status=record["company"].get(
                    "listing_status"
                ),
                market_cap=record["company"].get(
                    "market_cap"
                ),
                market_cap_category=record[
                    "company"
                ].get("market_cap_category"),
                listing_date=record["company"].get(
                    "listing_date"
                ),
                face_value=record["company"].get(
                    "face_value"
                ),
                website=record["company"].get(
                    "website"
                ),
                headquarters=record["company"].get(
                    "headquarters"
                ),
                business_description=record[
                    "company"
                ].get("business_description"),
            )

            financials = CompanyFinancials(
                symbol=record["financials"][
                    "symbol"
                ],
                revenue=record["financials"].get(
                    "revenue"
                ),
                net_profit=record[
                    "financials"
                ].get("net_profit"),
                eps=record["financials"].get(
                    "eps"
                ),
                book_value=record[
                    "financials"
                ].get("book_value"),
                roe=record["financials"].get(
                    "roe"
                ),
                roce=record["financials"].get(
                    "roce"
                ),
                debt_to_equity=record[
                    "financials"
                ].get("debt_to_equity"),
                operating_margin=record[
                    "financials"
                ].get("operating_margin"),
                promoter_holding=record[
                    "financials"
                ].get("promoter_holding"),
                dividend_yield=record[
                    "financials"
                ].get("dividend_yield"),
            )

            intelligence = CompanyIntelligence(
                company=company,
                financials=financials,
            )

            records.append(
                {
                    "intelligence": intelligence,
                    "screening": record[
                        "screening"
                    ],
                }
            )

        return records