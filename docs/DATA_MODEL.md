# Data Model

## Company Model

The Company model represents the core company entity used throughout the ICI project. It serves as the shared data structure between collectors, validators, and downstream processing.

### Fields

- symbol: the primary ticker or trading symbol for the company.
- company_name: the human-readable company name.
- isin: the International Securities Identification Number, when available.
- nse_code: the company identifier used on the National Stock Exchange.
- bse_code: the company identifier used on the Bombay Stock Exchange.
- sector: the company sector classification.
- industry: the company industry classification.
- exchange: the exchange where the security is listed.
- listing_status: the current listing status of the company or instrument.
- market_cap: the market capitalization value, where available.

## Purpose

This model provides a shared structure for representing core company metadata in a consistent and extensible way.

## Planned Future Models

The project may evolve to include additional models such as:

- FinancialStatement for financial reporting data.
- ShareholdingPattern for ownership and shareholding information.
- CorporateAction for corporate events and actions.
- PriceHistory for historical price and market movement data.

## Design Goals

The data model is designed to:
- Keep domain models independent of data sources.
- Support strong typing and validation.
- Remain extensible as additional financial datasets are introduced.
- Promote consistency across collectors and downstream processing.
