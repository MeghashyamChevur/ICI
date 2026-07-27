from pathlib import Path

from ici.collectors.company_master.sources import (
    CompanyMasterSource,
    FileCompanyMasterSource,
    NseCompanyMasterSource,
    CompanyMasterSourceFactory,
)


def test_factory_returns_file_source_for_file_selector() -> None:
    factory = CompanyMasterSourceFactory()
    source = factory.create("file")

    assert isinstance(source, CompanyMasterSource)
    assert isinstance(source, FileCompanyMasterSource)
    assert source.path == Path("tests/data/company_master_sample.csv")


def test_factory_returns_nse_source_for_nse_selector() -> None:
    factory = CompanyMasterSourceFactory()
    source = factory.create("nse")

    assert isinstance(source, CompanyMasterSource)
    assert isinstance(source, NseCompanyMasterSource)
