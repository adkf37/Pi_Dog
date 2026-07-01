# Task 01 — Scaffold Repo

**Phase:** 0 — Scaffolding
**Profile:** build
**Dependencies:** None
**Status:** pending

## Description

Create the Python package structure under `src/pidog_brain/`, including `pyproject.toml`, `README.md`, `.env.example`, and the full module tree.

## Inputs

- `project_overview.md` — sections 10, 11 (repo scaffold, key files)

## Outputs

- `src/pidog_brain/__init__.py`
- `src/pidog_brain/main.py` (stub CLI entry point)
- `src/pidog_brain/config.py` (stub)
- `src/pidog_brain/llm/__init__.py`
- `src/pidog_brain/planner/__init__.py`
- `src/pidog_brain/robot/__init__.py`
- `src/pidog_brain/perception/__init__.py`
- `src/pidog_brain/speech/__init__.py`
- `src/pidog_brain/runtime/__init__.py`
- `scripts/setup_pi.sh` (stub)
- `.env.example`
- `pyproject.toml`
- `README.md` (top-level project readme)

## Acceptance Checks

- [ ] `pip install -e .` succeeds
- [ ] `python -c "import pidog_brain; print('ok')"` succeeds
- [ ] `pytest` runs (even if 0 tests collected)
- [ ] `README.md` exists with hardware requirements, quick start, and safety notes
