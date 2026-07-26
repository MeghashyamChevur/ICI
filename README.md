# Indian Compounder Index (ICI)

## Project Overview

The Indian Compounder Index (ICI) is a Python-based project scaffold for building a data pipeline around Indian listed companies, financial metrics, scoring logic, and reporting workflows. The repository is organized to support future development of extraction, transformation, validation, scoring, and report generation steps.

## Objectives

- Provide a clean and modular project structure for data-focused Python development.
- Separate raw, processed, master, and source data assets clearly.
- Support future implementation of validation, scoring, and reporting features.
- Encourage Python best practices such as package organization, dependency management, and testing.

## Folder Structure

```text
ICI/
├── config/                  # Configuration files and environment settings
├── data/
│   ├── raw/                 # Raw ingested data
│   ├── processed/           # Cleaned and transformed data
│   ├── master/              # Master reference and lookup data
│   └── sources/             # Metadata for external data sources
├── docs/                    # Project documentation
├── excel/                   # Excel export outputs
├── logs/                    # Runtime and application logs
├── reports/                 # Generated reports
├── scripts/
│   ├── extract/             # Data extraction scripts
│   ├── transform/           # Data transformation scripts
│   ├── validate/            # Data validation scripts
│   ├── scoring/             # Scoring logic scripts
│   └── reports/             # Report generation scripts
├── tests/                   # Automated tests
├── ici/                     # Main Python package
├── .github/workflows/       # CI/CD workflow definitions
└── README.md                # Project documentation
```

## Technology Stack

- Python 3.10+
- pandas for data manipulation
- numpy for numerical operations
- openpyxl for Excel support
- requests and beautifulsoup4 for data collection
- lxml for HTML and XML parsing
- matplotlib for visualization support
- pydantic for data validation
- typer for CLI development
- pytest for automated testing
- python-dotenv for environment management

## Roadmap

- Phase 1: Establish the project scaffold, package structure, and documentation.
- Phase 2: Implement extraction and transformation pipelines for source data.
- Phase 3: Introduce validation rules and quality checks.
- Phase 4: Add scoring, reporting, and export workflows.
- Phase 5: Expand automation with CI/CD and testing coverage.
