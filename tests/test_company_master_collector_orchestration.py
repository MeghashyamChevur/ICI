from typing import Any

from ici.collectors.company_master.collector import CompanyMasterCollector
from ici.collectors.company_master.exceptions import CompanyMasterValidationError
from ici.collectors.company_master.normalizer import CompanyMasterNormalizer
from ici.collectors.company_master.parser import CompanyMasterParser
from ici.collectors.company_master.persistence import CompanyMasterPersistence
from ici.collectors.company_master.sources import CompanyMasterSource
from ici.models.company import Company


class StubSource(CompanyMasterSource):
    def download(self) -> dict[str, Any]:
        return {"records": [{"symbol": "reliance", "company_name": "Reliance Industries"}]}

    def fetch(self) -> dict[str, Any]:
        return self.download()


class StubParser(CompanyMasterParser):
    def parse(self, payload: Any) -> list[Company]:
        return [Company(symbol="reliance", company_name="Reliance Industries")]


class StubNormalizer(CompanyMasterNormalizer):
    def normalize(self, company: Company) -> Company:
        return Company(symbol="RELIANCE", company_name="Reliance Industries")


class StubValidator:
    def validate(self, company: Company) -> Company:
        if not company.symbol or not company.company_name:
            raise CompanyMasterValidationError("invalid")
        return company


class StubPersistence(CompanyMasterPersistence):
    def __init__(self) -> None:
        self.saved: list[Company] = []

    def save(self, items: list[Company]) -> None:
        self.saved.extend(items)


def test_collect_orchestrates_pipeline_with_dependencies() -> None:
    source = StubSource()
    parser = StubParser()
    normalizer = StubNormalizer()
    persistence = StubPersistence()

    collector = CompanyMasterCollector(source=source, parser=parser, normalizer=normalizer, persistence=persistence)
    collector.validate = StubValidator().validate  # type: ignore[assignment]

    result = collector.collect()

    assert len(result) == 1
    assert result[0].symbol == "RELIANCE"
    assert persistence.saved[0].symbol == "RELIANCE"
