# Architecture

## Purpose

The Indian Compounder Index (ICI) is a Python-based project for collecting company-related data, validating it, and preparing the foundation for scoring and reporting workflows. The system is designed to support structured, extensible analysis of Indian listed companies without coupling data collection, validation, and reporting into a single layer.

## Modular Architecture

The project is organized around a small set of focused modules:

- CLI: provides entry points for project initialization and workflow actions.
- Collectors: encapsulate data collection responsibilities and expose a common interface.
- Validators: validate collected records before they enter downstream processing.
- Models: define the domain objects used throughout the pipeline.
- Data Storage: separates raw, processed, master, and cache data into clearly defined locations.
- Scoring Engine: will evaluate collected data according to business rules and ranking logic.
- Reports: will produce human-readable outputs such as summaries and exports.

## High-Level Data Flow

1. The CLI triggers a workflow command.
2. A collector retrieves source data or prepares a placeholder record set.
3. Validators review the collected data for structural correctness.
4. Validated records are represented through domain models.
5. Data is persisted in the appropriate data storage location.
6. The scoring engine and reporting layers consume the prepared data.

## Design Principles

- Modularity: each responsibility is isolated in its own package or module.
- Extensibility: new collectors and validators can be added without rewriting the surrounding workflow.
- Strong Typing: Python type hints are used throughout the codebase to improve clarity and maintainability.
- Testing: automated tests cover core package behavior and architectural components.
- Separation of Concerns: data collection, validation, modeling, scoring, and reporting remain distinct responsibilities.

## Current Implementation Status

### Completed Milestones

- Project Foundation
- Core Framework
- Collector Architecture
- Company Model
- Validator Framework
- Unit Tests

### Planned Milestones

- Company Master Collector
- Financial Statement Collectors
- Scoring Engine
- Reports
- Dashboard
