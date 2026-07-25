# Indian Compounder Index (ICI)

A production-ready Python platform for analyzing Indian listed companies and generating a composite investment index based on compounding metrics.

## Overview

ICI is designed to help investors and researchers:
- Extract and aggregate financial data from Indian listed companies
- Validate data quality and consistency
- Calculate composite scoring metrics
- Generate insights and reports on investment opportunities
- Identify long-term wealth-building stocks

## Project Structure

```
ICI/
├── config/                 # Configuration files
├── data/                   # Data storage
│   ├── raw/               # Original downloaded data
│   ├── processed/         # Cleaned and processed data
│   ├── master/            # Master reference data
│   └── sources/           # Source definitions
├── docs/                  # Documentation
├── excel/                 # Excel outputs
├── logs/                  # Application logs
├── reports/               # Generated reports
├── scripts/               # Data processing scripts
│   ├── extract/           # Data extraction
│   ├── transform/         # Data transformation
│   ├── validate/          # Data validation
│   ├── scoring/           # Scoring algorithms
│   └── reports/           # Report generation
├── tests/                 # Unit and integration tests
├── ici/                   # Main Python package
│   ├── __init__.py
│   ├── config.py          # Path and directory configuration
│   ├── settings.py        # Application settings
│   ├── logger.py          # Logging configuration
│   ├── cli.py             # Command-line interface
│   └── utils.py           # Utility functions
└── .github/
    └── workflows/         # GitHub Actions workflows
```

## Technology Stack

- **Python 3.12**: Core language
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file handling
- **requests**: HTTP requests
- **beautifulsoup4**: Web scraping
- **lxml**: XML/HTML processing
- **numpy**: Numerical computing
- **matplotlib**: Data visualization
- **pydantic**: Data validation
- **typer**: CLI framework
- **pytest**: Testing framework
- **python-dotenv**: Environment variables

## Installation

### Prerequisites
- Python 3.12 or higher
- pip and virtualenv

### Setup

1. Clone the repository:
```bash
git clone https://github.com/MeghashyamChevur/ICI.git
cd ICI
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the project:
```bash
python -m ici.cli init
```

## Usage

### Command-Line Interface

The ICI platform is controlled via the command-line interface:

```bash
# Initialize project structure and directories
python -m ici.cli init

# Collect data from sources
python -m ici.cli collect

# Validate collected data
python -m ici.cli validate

# Calculate scoring metrics
python -m ici.cli score

# Export processed data
python -m ici.cli export

# Generate comprehensive reports
python -m ici.cli report
```

## Configuration

Configuration is managed through:
- `ici/settings.py`: Application-wide settings
- `.env` file: Environment-specific variables (create from `.env.example`)
- `config/`: Configuration files (YAML, JSON, etc.)

## Logging

All application logs are written to `logs/ici.log` with console output for real-time feedback.

## Testing

Run tests using pytest:

```bash
pytest                    # Run all tests
pytest -v                # Verbose output
pytest --cov            # With coverage report
```

Tests are automatically run on every push and pull request via GitHub Actions.

## Development

### Code Standards
- Follows PEP 8 style guidelines
- Type hints on all functions
- Comprehensive docstrings
- Unit tests for all modules

### Contributing
1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

Meghashyam Chevur

## Roadmap

### Phase 1 (Current): Foundation
- ✅ Project structure and CLI framework
- ✅ Logging and configuration
- ⏳ Data collection infrastructure
- ⏳ Data validation framework

### Phase 2: Core Features
- Data extraction from multiple sources
- Financial metrics calculation
- Scoring algorithm implementation
- Excel report generation

### Phase 3: Advanced Features
- Web dashboard
- API endpoints
- Real-time data updates
- Advanced analytics

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
