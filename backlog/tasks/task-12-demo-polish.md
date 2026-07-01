# Task 12 — Demo & Polish

**Phase:** 5 — Demo & Polish
**Profile:** build / scribe
**Dependencies:** task-08, task-10, task-11
**Status:** pending

## Description

Create the final demo packaging: one-command demo script, a set of 5–8 scripted prompts that exercise the system, model benchmark logging, telemetry improvements, and final documentation refresh.

This task is the closeout phase. All prior tasks must be complete before this runs. The deliverable is a polished demo that works end-to-end in both `--mode mock` (developer laptop) and `--mode robot` (PiDog hardware).

## Inputs

- Task 08 output (CLI entry point)
- Task 10 output (voice loop)
- Task 11 output (sensor reactions)
- `project_overview.md` section 16 (benchmark table), section 17 (demo definition)

## Outputs

- `scripts/run_text_demo.sh` — one-command demo launcher
- `scripts/run_robot_demo.sh` — hardware demo launcher
- `scripts/run_voice_demo.sh` — voice demo launcher
- `docs/model_benchmarks.md` — benchmark results table
- `docs/demo_plan.md` — demo script with 5–8 prompts and expected behavior
- Updates to `src/pidog_brain/runtime/logging.py` and `telemetry.py` if needed
- Final review and update of `README.md`, `docs/hardware_setup.md`, `docs/action_vocabulary.md`

## Acceptance Checks

- [ ] `./scripts/run_text_demo.sh` works in mock mode on any laptop
- [ ] `./scripts/run_robot_demo.sh` works on PiDog hardware
- [ ] `./scripts/run_voice_demo.sh` works on PiDog hardware with audio
- [ ] 5–8 scripted prompts each return validated actions (no crashes)
- [ ] Log output includes model name, response latency, parse success/failure, executed actions
- [ ] `docs/model_benchmarks.md` has at minimum the table header and one model row filled
- [ ] All documentation files are internally consistent
