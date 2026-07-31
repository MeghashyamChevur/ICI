"""Persistence for company intelligence."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ici.models import CompanyIntelligence


class CompanyIntelligencePersistence:
    """Persist company intelligence data."""

    def save(
        self,
        intelligence: list[CompanyIntelligence],
        output_path: Path,
    ) -> None:
        """Save company intelligence data as JSON."""

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = [
            asdict(company_intelligence)
            for company_intelligence in intelligence
        ]

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=2,
            )