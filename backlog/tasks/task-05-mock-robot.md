# Task 05 — Mock Robot

**Phase:** 0 — Scaffolding
**Profile:** build
**Dependencies:** task-03
**Status:** pending

## Description

Implement `src/pidog_brain/robot/` with `base.py` (abstract robot interface), `mock_robot.py` (logs actions to console), and `actions.py` (action → method mapping). The mock robot must work on any laptop without PiDog hardware.

## Inputs

- Task 03 output (`schema.py` with action vocabulary)
- `project_overview.md` sections 8, 11

## Outputs

- `src/pidog_brain/robot/__init__.py`
- `src/pidog_brain/robot/base.py` — abstract `RobotBase` class
- `src/pidog_brain/robot/mock_robot.py` — `MockRobot` impl
- `src/pidog_brain/robot/actions.py` — action name → method dispatch

## Acceptance Checks

- [ ] `MockRobot` implements all 14 actions from vocabulary
- [ ] Each action call is logged with action name and duration
- [ ] `MockRobot` returns a structured result after each action
- [ ] No PiDog hardware imports in mock path
- [ ] Unit tests verify mock robot behavior
