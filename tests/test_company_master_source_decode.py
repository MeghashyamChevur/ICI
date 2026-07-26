from pathlib import Path

import pytest

from ici.collectors.company_master.exceptions import CompanyMasterSourceDecodeError, CompanyMasterSourceDownloadError
from ici.collectors.company_master.sources import FileCompanyMasterSource


def test_decode_returns_raw_records_from_csv_fixture() -> None:
    sample_path = Path(__file__).parent / "data" / "company_master_sample.csv"
    source = FileCompanyMasterSource(path=sample_path)

    records = source.fetch()

    assert len(records) == 2
    assert records[0]["symbol"] == "RELIANCE"
    assert records[1]["company_name"] == "Tata Consultancy Services"


def test_decode_raises_source_exception_for_missing_file() -> None:
    source = FileCompanyMasterSource(path=Path("tests/data/missing.csv"))

    with pytest.raises(CompanyMasterSourceDownloadError):
        source.fetch()
