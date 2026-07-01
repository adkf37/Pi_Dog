# Task 07 — Planner

**Phase:** 1 — LLM Integration
**Profile:** build
**Dependencies:** task-03, task-04, task-06
**Status:** pending

## Description

Implement `src/pidog_brain/planner/` — build prompt with system prompt + user input + robot state, call LLM, parse JSON response, validate through policy, and return a safe `RobotPlan`.

## Inputs

- Task 03 output (`schema.py`)
- Task 04 output (`policy.py`)
- Task 06 output (`ollama_client.py`)

## Outputs

- `src/pidog_brain/planner/prompts.py` — system prompt + action schema description
- `src/pidog_brain/planner/parser.py` — JSON response parser with retry
- `src/pidog_brain/planner/__init__.py` — main `Planner` class orchestrating the flow

## Acceptance Checks

- [ ] `Planner.plan(user_input, robot_state)` returns a validated `RobotPlan`
- [ ] Invalid JSON from LLM is retried or returns a safe fallback
- [ ] Policy violations in LLM output are caught before returning
- [ ] Unit tests with mock LLM returning valid/invalid/malformed responses
