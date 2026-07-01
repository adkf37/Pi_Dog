# Task 08 — CLI Demo

**Phase:** 1 — LLM Integration
**Profile:** build
**Dependencies:** task-02, task-05, task-07
**Status:** pending

## Description

Implement `src/pidog_brain/main.py` as a CLI entry point that accepts `--mode`, `--input`, and other flags. Wire up config → planner → mock robot (or PiDog adapter) → output.

## Inputs

- Task 02 output (config)
- Task 05 output (mock robot)
- Task 07 output (planner)

## Outputs

- Complete `src/pidog_brain/main.py` with `argparse` CLI

## Acceptance Checks

- [ ] `python -m pidog_brain.main --mode mock --input "hello"` prints validated actions
- [ ] `--mode robot` selects the real PiDog adapter (safe to fail if no hardware)
- [ ] `--bench` flag disables movement
- [ ] Log output includes model name, response latency, parse success/failure, executed actions
