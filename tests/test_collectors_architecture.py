from ici.collectors.company_master import CompanyMasterCollector
from ici.collectors.registry import CollectorRegistry, get_registry
from ici.exceptions import CollectorError, ValidationError
from ici.models.company import Company
from ici.validators.validator import BaseValidator, ValidationResult


def test_company_model_defaults() -> None:
    company = Company(symbol="RELIANCE", company_name="Reliance Industries")
    assert company.symbol == "RELIANCE"
    assert company.company_name == "Reliance Industries"
    assert company.market_cap is None


def test_company_master_collector_collects_empty_placeholder() -> None:
    collector = CompanyMasterCollector()
    assert collector.collect() == []


def test_company_master_collector_validation_requires_symbol_and_name() -> None:
    collector = CompanyMasterCollector()
    valid = Company(symbol="TCS", company_name="Tata Consultancy Services")
    invalid = Company(symbol="", company_name="")
    assert collector.validate(valid) is True
    assert collector.validate(invalid) is False


def test_registry_register_and_get() -> None:
    registry = CollectorRegistry()
    registry.register(CompanyMasterCollector)
    assert registry.get("company_master") is CompanyMasterCollector
    assert "company_master" in registry.list()


def test_registry_module_instance() -> None:
    registry = get_registry()
    assert registry.get("company_master") is CompanyMasterCollector


def test_validator_returns_validation_result() -> None:
    validator = BaseValidator[Company]()
    result = validator.validate(Company(symbol="INFY", company_name="Infosys"))
    assert isinstance(result, ValidationResult)
    assert result.is_valid is True


def test_custom_exceptions_are_available() -> None:
    assert issubclass(CollectorError, Exception)
    assert issubclass(ValidationError, Exception)
