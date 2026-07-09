# Checkpoint Brief - before-closeout

Project: Pi_Dog
Checkpoint: before-closeout
Return Phase: closeout
Generated: 2026-07-09

## What Happened Since The Last Checkpoint

- Build Batch 6 (task-08 CLI Demo) implemented — `main.py` wires config → LLM → Planner → MockRobot; 9 tests added, 55/55 total passing. See `.maestro/decisions.md` decisions 019–022.
- Critic phase completed — 7 warn findings across tasks 07–09, 12, and lint infra. Verdict: Warn. See `.maestro/critic_report.md`.
- Previous 3 blocking issues (phase mismatch, CLI skeleton, SC3) all resolved or accepted as wontfix. Lint infra partially resolved (ruff config but not installable).
- 7 open FEEDBACK.md entries remain, all from the critic. Notable: mock mode uses real Ollama client (not MockLLM), prompt constraints hardcoded, `--mode robot` silently falls back to MockRobot, no task-08 validation report exists.
- Tasks 09–12 remain pending (PiDog Adapter, Voice Loop, Sensor Reactions, Demo & Polish).

## What Will Be Spent Next

- **Task-09 (PiDog Adapter, Batch 7):** ~1 build session. Implements `PiDogAdapter` with guarded import, maps all 14 actions.
- **Task-12 (Demo & Polish, Batch 9):** ~1 build + 1 scribe session. Demo scripts, docs refresh, closeout.
- **Cross-cutting cleanup (if prioritized):** Fix mock mode LLM, prompt constraints, robot fallback, SC3 disposition, ruff dependency. ~1 build session.
- **Validation passes:** task-08 validation report, then task-09 validation, then closeout validation. ~1–2 validator sessions.

## Questions

### Q1 - Fix critic findings before or after task-09 hardware bridge?
Question: The critic filed 7 warn findings in tasks 07-08 that affect mock-mode demo quality, prompt accuracy, and test coverage. Task-09 (PiDog Adapter) is the next build step but depends on task-08. Should these findings be fixed before starting task-09, or proceed to hardware bridge and fix them in a cleanup batch before closeout?
Options: Fix findings first (~1 build session), then proceed with task-09; Proceed to task-09 immediately, fix findings as part of Batch 9 (task-12) cleanup
Default: Fix findings first (~1 build session), then proceed with task-09
Decision: default

### Q2 - What should be done about SC3 (80% valid JSON from Ollama)?
Question: SC3 requires 80% valid JSON from a real Ollama endpoint but has no measurement infrastructure. The project has no plan to measure it. Should SC3 be removed from the success criteria, or explicitly added as a task-09 sub-task (hardware bring-up measurement script)?
Options: Remove SC3 from success criteria and update `backlog/README.md`; Add SC3 measurement as a task-09 sub-task (~0.5 session); Add SC3 measurement as a task-12 sub-task (~0.5 session)
Default: Remove SC3 from success criteria, update backlog/README.md
Decision: default

### Q3 - Should task-12 demos be scoped to only what is built (mock + text only)?
Question: Task-12 depends on tasks 08, 10, and 11 (all must be complete). If time or hardware constraints prevent completing tasks 10 (Voice) and 11 (Sensors), should task-12 produce a mock-only/text-only demo that works on a laptop and defers voice/hardware scripts, or should task-12 block until all prior tasks are done?
Options: Scope task-12 to mock+text only, defer voice/robot demo scripts; Block task-12 until tasks 10 and 11 are complete
Default: Scope task-12 to mock+text only, defer voice/robot demo scripts
Decision: default
