# AGENTS.md

## Project Overview

Desktop application (Python 3.14+) for managing compartmental ODE models
with their parameters, compartments, and associated scientific literature.
Goal: store and process models for Symbolic Regression (classic and ML).
Stack: Peewee (ORM), Sympy (symbolic). Architecture: Clean Architecture. License: MIT.

## Repository Structure

- src/database/ — Peewee entities and DB configuration
- src/dtos/ — dataclasses
- src/gui/ — graphical user interface
- src/services/ — business logic
- src/scripts/ — I/O automations
- src/main.py — entry point
- tests/unit/ — unit tests
- tests/integration/ — integration tests
- data/ — example datasets (read-only) + generated model JSONs
- docs/ — project documentation
- .opencode/skill/ — agent skills (e.g., pdf_to_ode_json.md for PDF to JSON conversion)

## Setup

    pip install -r requirements.txt

## Commands

    # All tests
    pytest -v

    # Unit tests only (in-memory SQLite)
    pytest tests/unit -v

    # Integration tests only
    pytest tests/integration -v

    # Single test
    pytest tests/unit/test_<name>.py -v

    # Debug
    pytest tests/unit/test_<name>.py -k "test_name" --pdb

## Code Style

- Type hints required always.
- Google-style docstrings.
- PEP 8; type vars use CapWords short names (`T`, `AnyStr`), with `_co`/`_contra` suffixes only for variance.
- Validate inputs at boundaries (fail fast).

## Testing

- Naming: `test_<unit>_<scenario>_<expected>`.
- Minimum coverage: unit >=90%, integration >=70%.
- tests/unit uses in-memory SQLite; tests/integration uses testcontainers.
- Before commit: pytest + pip-audit must pass.

## Guardrails (Never do)

- Do not modify existing files in data/ (adding new model JSONs is allowed)
- Do not edit already-applied Peewee migrations; create a new one.
- Do not commit .env, secrets, or PII data.
- Do not add new dependencies without justifying it in the PR.
- Do not commit directly to main or develop.
- Do not modify files in specs/.

## PR Instructions

- Branch: `feature/<name>` or `bugfix/<name>` from `develop`; `hotfix/<v>` from `main`.
- Title: `[<module>] <short description>`.
- Before opening PR: pytest and pip-audit green.
- Data schema: docs/data-models.md.

## Spec-Driven Development

- Specs live in `specs/NNN-<feature>/` with `requirements.md`, `design.md`, `tasks.md`.
- Before implementing a feature, read the corresponding spec files.
- Follow `tasks.md` in order; verify each task before moving to the next.
- If code and spec diverge, the spec wins — update the code, not the spec.

## Agent Skills

- Skills live in `.opencode/skill/` and provide specialized workflows
- **pdf_to_ode_json.md**: Convert PDF articles to ODE model JSON files for the encyclopedia
  - Usage: Follow the skill's process to extract models from PDFs and create JSON in `data/`
  - Output: One JSON per article named `{year}_{topic}_model.json`
  - Validates: JSON structure only (no database import required)
