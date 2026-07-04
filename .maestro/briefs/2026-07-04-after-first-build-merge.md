# Checkpoint Brief - after-first-build-merge

Project: Pi_Dog
Checkpoint: after-first-build-merge
Return Phase: validate
Generated: 2026-07-04

## What Happened Since The Last Checkpoint
- Build Batch 5 (task-07 Planner) implemented — `planner/__init__.py`, `parser.py` (brace-matching JSON extraction), `prompts.py` (action descriptions from `robot/actions.py`), fallback plan on LLM/parse/policy failure. See `.maestro/decisions.md` decisions 014–017.
- 46 tests passing (up from 29 at last checkpoint) — 17 planner tests added; all prior tests continue to pass.
- OllamaClient (task-06) remains un-validated — no mocked HTTP tests yet despite being committed in the previous batch.

## What Will Be Spent Next
- **Batch 6 — task-08 (CLI Demo):** Wire `main.py` to config + planner + mock robot for end-to-end `python -m pidog_brain.main --mode mock --input "hello"`. ~1 build session.
- **Validation (tasks 06–07):** Add mocked HTTP tests for OllamaClient and run planner acceptance checks. ~0.5 validator session.

## Questions

### Q1 - Should task-08 proceed without waiting for a dedicated validator pass on tasks 06–07?
Question: The deliverable pace has been build-forward without blocking on validation between batches. task-08 depends on task-07 (done) and task-05 (done), which are both already tested at the unit level. Should task-08 proceed immediately, or pause for a dedicated validator session on tasks 06–07 before the CLI integration work begins?
Options: Proceed to task-08 immediately, validating concurrently or after; Pause for dedicated validator pass on tasks 06–07 before starting CLIDemo
Default: Proceed to task-08 immediately, validating concurrently or after
Decision: default

### Q2 - Should mock mode remain the primary test target for task-08?
Question: task-08 acceptance says `python -m pidog_brain.main --mode mock --input "hello"` works end-to-end. The mock robot (task-05) is fully implemented. Is there appetite for a `--mode ollama` path in the CLI demo in this batch, or should that wait until task-09 (hardware bridge) when real robot output can be observed?
Options: Mock mode only for task-08; Add --mode ollama to CLI demo in this batch
Default: Mock mode only for task-08
Decision: default
