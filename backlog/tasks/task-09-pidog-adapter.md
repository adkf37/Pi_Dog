# Task 09 — PiDog Adapter

**Phase:** 2 — Hardware Bridge
**Profile:** build
**Dependencies:** task-05, task-08
**Status:** pending

## Description

Implement `src/pidog_brain/robot/pidog_adapter.py` wrapping SunFounder's PiDog library methods behind the repo's action vocabulary. This must be the only file importing PiDog-specific hardware libraries. Also add hardware setup documentation.

## Inputs

- Task 05 output (`actions.py`, `base.py`)
- SunFounder PiDog docs and examples
- `project_overview.md` sections 4, 5, 12 (Milestone 1)

## Outputs

- `src/pidog_brain/robot/pidog_adapter.py` — `PiDogAdapter` implementing `RobotBase`
- `docs/hardware_setup.md` — Pi OS setup, SunFounder library install, calibration, smoke tests

## Acceptance Checks

- [ ] `PiDogAdapter` maps all 14 actions to PiDog library calls
- [ ] Movement actions are disabled when `movement_enabled=False`
- [ ] Robot always returns to stable posture after action sequence
- [ ] Hardware imports (`pidog`, `robot-hat`, `vilib`) are isolated to this file
- [ ] `pip install` / import works on non-Pi machines (import skipped or guarded)
