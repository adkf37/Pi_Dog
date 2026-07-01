# Task 11 — Sensor Reactions

**Phase:** 4 — Sensor Reactions
**Profile:** build
**Dependencies:** task-07, task-09
**Status:** pending

## Description

Implement touch sensor and ultrasonic sensor handlers for the PiDog. Create the main async event loop that listens for sensor events and routes them to pre-defined safety behaviors or to the LLM planner for personality-rich responses.

Sensor events must bypass or constrain the LLM when speed matters — e.g. ultrasonic obstacle triggers an immediate stop/backup without waiting for LLM inference. The LLM may add personality commentary only *after* the safety action is taken.

## Inputs

- Task 07 output (planner)
- Task 09 output (PiDog adapter)
- `project_overview.md` section 12 (Milestone 5)

## Outputs

- `src/pidog_brain/perception/sensors.py` — touch + ultrasonic sensor event handlers
- `src/pidog_brain/runtime/event_loop.py` — async main event loop (sensor polling, action dispatch)
- `src/pidog_brain/runtime/__init__.py`

## Acceptance Checks

- [ ] Touch sensor (front/rear) triggers a pre-defined behavior (e.g. happy wiggle, avoid)
- [ ] Ultrasonic sensor detects obstacle within configurable threshold
- [ ] Ultrasonic obstacle triggers safe stop / backup within 500ms
- [ ] Sensor-triggered safety actions fire without waiting for LLM
- [ ] LLM can add personality response after the safety action completes
- [ ] Sensor polling and action execution are non-blocking with respect to LLM inference
- [ ] Unit tests with simulated sensor events
