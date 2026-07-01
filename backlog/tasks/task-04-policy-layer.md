# Task 04 — Policy Layer

**Phase:** 0 — Scaffolding
**Profile:** build
**Dependencies:** task-03
**Status:** pending

## Description

Implement `src/pidog_brain/planner/policy.py` to validate and sanitize every `RobotPlan` before execution. Reject invalid actions, cap sequence length, clamp durations, block movement in bench mode, and enforce the allow-list.

## Inputs

- Task 03 output (`schema.py` with `RobotPlan`, `RobotAction`, `AllowedAction`)
- `project_overview.md` sections 8, 13 (safety rules)

## Outputs

- `src/pidog_brain/planner/policy.py` — `validate_plan(plan, config) -> RobotPlan` function

## Acceptance Checks

- [ ] Invalid action names are rejected
- [ ] Plans with > `MAX_ACTIONS_PER_TURN` actions are rejected
- [ ] Durations > `MAX_ACTION_DURATION_S` are clamped or rejected
- [ ] Movement actions (`step_forward`, `turn_left`, etc.) are blocked in bench mode
- [ ] Valid plans pass through unchanged
- [ ] Unit tests cover all rejection paths
