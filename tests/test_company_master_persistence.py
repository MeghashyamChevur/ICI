from pathlib import Path
import csv

from ici.collectors.company_master.persistence import CompanyMasterPersistence
from ici.models.company import Company


def test_save_writes_csv_with_deterministic_columns(tmp_path: Path) -> None:
    output_path = tmp_path / "exports" / "companies.csv"
    persistence = CompanyMasterPersistence(output_path)
    companies = [
        Company(symbol="reliance", company_name="Reliance Industries", exchange="NSE", listing_status="Active", market_cap=100.5),
        Company(symbol="tcs", company_name="Tata Consultancy Services", exchange="BSE", listing_status="Delisted"),
    ]

    written_path = persistence.save(companies)

    assert written_path == output_path
    assert output_path.exists()
    assert output_path.parent.exists()

    with output_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert rows[0]["symbol"] == "reliance"
    assert rows[0]["company_name"] == "Reliance Industries"
    assert rows[0]["exchange"] == "NSE"
    assert rows[0]["listing_status"] == "Active"
    assert rows[0]["market_cap"] == "100.5"
    assert rows[1]["market_cap"] == ""


def test_load_reads_company_instances_from_csv(tmp_path: Path) -> None:
    output_path = tmp_path / "exports" / "companies.csv"
    persistence = CompanyMasterPersistence(output_path)
    companies = [Company(symbol="INFY", company_name="Infosys", exchange="NSE", listing_status="Active")]

    persistence.save(companies)
    loaded = persistence.load()

    assert len(loaded) == 1
    assert loaded[0].symbol == "INFY"
    assert loaded[0].company_name == "Infosys"
    assert loaded[0].exchange == "NSE"
    assert loaded[0].listing_status == "Active"
