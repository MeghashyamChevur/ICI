"""Persistence for ranked companies."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ici.models import (
    Company,
    CompanyFinancials,
    RankingResult,
)


class CompanyRankingPersistence:
    """Persist ranked companies."""

    def save(
        self,
        companies: list[dict[str, object]],
        output_path: Path,
    ) -> None:
        """Save ranked companies to JSON."""

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output: list[dict[str, object]] = []

        for company in companies:
            company_data = company["company"]
            financials_data = company["financials"]
            screening_data = company["screening"]
            ranking_data = company["ranking"]

            output.append(
                {
                    "company": (
                        asdict(company_data)
                        if isinstance(company_data, Company)
                        else company_data
                    ),
                    "financials": (
                        asdict(financials_data)
                        if isinstance(financials_data, CompanyFinancials)
                        else financials_data
                    ),
                    "screening": screening_data,
                    "ranking": (
                        ranking_data.to_dict()
                        if isinstance(
                            ranking_data,
                            RankingResult,
                        )
                        else ranking_data
                    ),
                }
            )

        with output_path.open(
            mode="w",
            encoding="utf-8",
        ) as file:
            json.dump(
                output,
                file,
                indent=2,
            )