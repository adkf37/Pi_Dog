# Task 02 — Implement Config

**Phase:** 0 — Scaffolding
**Profile:** build
**Dependencies:** task-01
**Status:** pending

## Description

Implement `src/pidog_brain/config.py` to read settings from environment variables / `.env` file with sane defaults. Support `mock` and `robot` modes, LLM backend selection, Ollama host/model, bench mode, action limits, and feature toggles.

## Inputs

- `.env.example` from task-01
- `project_overview.md` section 11 (`.env.example`)

## Outputs

- `src/pidog_brain/config.py` — complete implementation with Pydantic Settings or dataclass

## Acceptance Checks

- [ ] Config reads `PIDOG_MODE`, `LLM_BACKEND`, `OLLAMA_HOST`, `OLLAMA_MODEL`, `BENCH_MODE`, `MAX_ACTIONS_PER_TURN`, `MAX_ACTION_DURATION_S` from env
- [ ] Defaults match `.env.example` when env vars are absent
- [ ] `BENCH_MODE=true` correctly sets `movement_enabled=False`
- [ ] Unit test coverage for all config fields
