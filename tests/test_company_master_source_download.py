from pathlib import Path

from ici.collectors.company_master.exceptions import CompanyMasterSourceDownloadError
from ici.collectors.company_master.sources import FileCompanyMasterSource


def test_download_returns_raw_response_body_from_csv_fixture() -> None:
    sample_path = Path(__file__).parent / "data" / "company_master_sample.csv"
    source = FileCompanyMasterSource(path=sample_path)

    payload = source.download()

    assert payload.startswith(b"symbol")
    assert b"RELIANCE" in payload


def test_download_raises_source_exception_on_missing_file() -> None:
    source = FileCompanyMasterSource(path=Path("tests/data/missing.csv"))

    try:
        source.download()
    except CompanyMasterSourceDownloadError:
        return

    raise AssertionError("Expected CompanyMasterSourceDownloadError")
