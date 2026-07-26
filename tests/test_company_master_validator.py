import pytest

from ici.collectors.company_master.exceptions import CompanyMasterValidationError
from ici.collectors.company_master.normalizer import CompanyMasterNormalizer
from ici.collectors.company_master.validator import CompanyMasterValidator
from ici.models.company import Company


def test_validate_many_returns_validated_companies() -> None:
    validator = CompanyMasterValidator()
    normalizer = CompanyMasterNormalizer()
    companies = [
        Company(symbol="reliance", company_name="Reliance Industries", exchange="nse", listing_status="active"),
        Company(symbol="tcs", company_name="Tata Consultancy Services", exchange="bse", listing_status="delisted"),
    ]

    validated = validator.validate_many(companies)
    normalized = normalizer.normalize_many(validated)

    assert len(validated) == 2
    assert validated[0].symbol == "reliance"
    assert validated[0].exchange == "nse"
    assert validated[0].listing_status == "active"
    assert normalized[0].symbol == "RELIANCE"
    assert normalized[0].exchange == "NSE"
    assert normalized[0].listing_status == "Active"
    assert normalized[1].listing_status == "Delisted"


def test_validate_many_raises_for_invalid_records() -> None:
    validator = CompanyMasterValidator()
    companies = [Company(symbol="", company_name=""), Company(symbol="INFY", company_name="Infosys")]

    with pytest.raises(CompanyMasterValidationError):
        validator.validate_many(companies)
