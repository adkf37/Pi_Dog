# Task 03 — Action Schema

**Phase:** 0 — Scaffolding
**Profile:** build
**Dependencies:** task-01
**Status:** pending

## Description

Define Pydantic models for the LLM output contract in `src/pidog_brain/planner/schema.py`. Include `RobotAction` (name, duration_s), `RobotPlan` (say, actions), and an `AllowedAction` enum with the initial 14-action vocabulary.

## Inputs

- `project_overview.md` sections 9, 11 (action vocabulary, schema definition)

## Outputs

- `src/pidog_brain/planner/schema.py` — Pydantic models

## Acceptance Checks

- [ ] Valid JSON parses into `RobotPlan` object
- [ ] Invalid action names raise validation error
- [ ] Negative durations raise validation error
- [ ] `AllowedAction` enum contains all 14 initial actions
- [ ] Unit tests validate schema parsing
