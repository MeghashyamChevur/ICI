from pathlib import Path

from ici.collectors.company_master.parser import CompanyMasterParser
from ici.collectors.company_master.sources import FileCompanyMasterSource


def test_source_records_are_parsed_into_company_models() -> None:
    sample_path = Path(__file__).parent / "data" / "company_master_sample.csv"
    source = FileCompanyMasterSource(path=sample_path)
    parser = CompanyMasterParser()

    decoded_records = source.fetch()
    companies = parser.parse({"records": decoded_records})

    assert len(companies) == 2
    assert companies[0].symbol == "RELIANCE"
    assert companies[0].company_name == "Reliance Industries"
    assert companies[1].symbol == "TCS"
