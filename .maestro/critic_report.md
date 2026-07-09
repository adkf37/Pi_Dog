# Critic Report — Pi_Dog

| Field | Value |
|---|---|
| Date | 2026-07-04 |
| Agent | critic |
| Checkpoint | before-closeout |
| Return Phase | closeout |

## Commands / Checks Attempted

```bash
pip install -e .                     # OK — installs successfully
python -m pytest tests/ -v           # 46/46 passed
python -c "import pidog_brain"       # OK
python -m pidog_brain.main --mode mock --input "say hello and wag your tail"
```

## Summary

The project has strong foundations: clean architecture, Pydantic schemas, typed exceptions, and 46 passing unit tests covering tasks 01–07. However, the project is **not ready for closeout**. Only 7 of 12 tasks are complete. The headline deliverable (CLI demo) does not function. A core acceptance criterion (80% valid JSON from Ollama) is not measurable.

## Adversarial Findings

### Finding 1 (BLOCK) — Phase mismatch: STATUS.md claims closeout with 5 tasks still pending

STATUS.md lists `Phase: closeout` but only tasks 01–07 are done. Tasks 08–12 are all `pending` in `.maestro/task_plan.md`:

| Task | Description | Status |
|------|-------------|--------|
| 08 | CLI Demo | pending |
| 09 | PiDog Adapter | pending |
| 10 | Voice Loop | pending |
| 11 | Sensor Reactions | pending |
| 12 | Demo & Polish | pending |

The STATUS.md `Next Action` field itself says "Proceed to Build Batch 6 (task-08 CLI Demo)" — this contradicts the closeout phase. 5 of 12 tasks (42%) remain unbuilt.

**Evidence:**
- `STATUS.md:5` — `Phase | closeout`
- `STATUS.md:14` — "Ready for Build Batch 6 (task-08 CLI Demo)"
- `.maestro/task_plan.md:14-18` — tasks 08–12 status = `pending`
- `backlog/README.md:11-16` — Success Criteria 2, 4, 6 depend on tasks 08–12

**What must change:** Reset `STATUS.md` phase to `build`. The project should return to build phase for Batch 6 before any closeout.

---

### Finding 2 (BLOCK) — Success Criterion 2 fails: CLI demo does not produce validated actions

The project's headline demo command — `python -m pidog_brain.main --mode mock --input "hello"` — prints configuration values and "Ready." It does **not** wire the planner, LLM client, or mock robot. No validated actions are produced.

**Evidence:**
- `src/pidog_brain/main.py:1-24` — Skeleton argparse with no planner/robot integration
- Terminal output: `PiDog Brain — mode=mock\nLLM backend=ollama model=tinyllama\nMovement enabled=False\nInput: say hello and wag your tail\nReady.`
- `backlog/README.md:12` — SC2: "runs on any laptop and prints validated actions"
- `backlog/tasks/task-08-cli-demo.md:24` — Acceptance: "prints validated actions"
- `.maestro/validation_report.md:50` — Validator noted "main.py: Basic argparse skeleton exists (task-08 not yet wired — expected, task-08 is pending)"

The validator correctly flagged this as "expected" and "pending", yet STATUS.md still advanced to closeout.

**What must change:** Implement task-08 (CLI Demo) before closeout can be considered.

---

### Finding 3 (BLOCK) — Success Criterion 3 is not measurable

SC3 requires "An Ollama-backed LLM on the Pi produces valid JSON (matching the action schema) at least 80% of the time." No integration test, benchmark, or measurement infrastructure exists to assess this threshold:

- All 17 planner tests use `MockLLM` or `RaisingLLM` — never a real Ollama endpoint.
- No prompt iteration or temperature tuning has been done to maximize valid JSON rate.
- The 80% threshold is aspirational with no data.

**Evidence:**
- `tests/test_planner.py:8-15` — `MockLLM` returns a hardcoded string; no real LLM integration
- `backlog/README.md:13` — SC3 text
- `src/pidog_brain/planner/prompts.py` — System prompt exists but has never been tested against Ollama output

**What must change:** At minimum, document a plan for measuring the valid-JSON rate against a real Ollama endpoint, or adjust SC3 to be testable in the current mock-first approach.

---

### Finding 4 (WARN) — OllamaClient acceptance tested only with mocked HTTP

Task-06 acceptance check #1 says "OllamaClient.generate(prompt) returns response text." All 8 tests use `respx`-mocked HTTP. The client has never been verified against a real Ollama API instance. Request/response payload compatibility, streaming behavior, and error recovery under real network conditions are untested.

**Evidence:**
- `.maestro/validation_report.md:24` — Task 06 check #1 result references `test_ollama_client_generates_text` which uses `respx_mock`
- `.maestro/decisions.md:108-109` — Validator acknowledges all tests use mocked HTTP

**Severity:** Warm — acceptable for a work-in-progress project, but the gap should be closed when real hardware is available.

---

### Finding 5 (WARN) — No lint/type-check infrastructure

The repo has no configured linter (ruff, flake8, pylint) or type checker (mypy, pyright). The validator acknowledged this but dismissed it as non-blocking. For a framework intended to run unattended on a Raspberry Pi, type errors that slip past tests could cause runtime crashes that are hard to debug headlessly.

**Evidence:**
- `.maestro/validation_report.md:54` — "No lint/type-check infrastructure configured in repo"
- `pyproject.toml` — No linting or type-checking tools configured

**Severity:** Warn — should be addressed before hardware deployment.

---

### Finding 6 (WARN) — Empty subpackages misrepresent completion

Three subpackages exist as empty `__init__.py` files only — `perception/`, `speech/`, `runtime/`. These correspond to tasks 10, 11 (voice/sensors/event loop) which are marked pending. While the structure is correctly scaffolded, a casual reviewer could mistake the presence of these directories for progress.

**Evidence:**
- `src/pidog_brain/perception/__init__.py` — empty
- `src/pidog_brain/speech/__init__.py` — empty
- `src/pidog_brain/runtime/__init__.py` — empty

**Severity:** Warn — documentation clarity.

## Verdict

**Block** — The project should return to the build phase before closeout.

Three blocking issues prevent closeout:
1. STATUS.md phase is inconsistent with reality (closeout vs. 5 pending tasks).
2. Success Criterion 2 fails — the CLI demo does not produce validated actions.
3. Success Criterion 3 is not measurable — the 80% valid-JSON threshold cannot be verified or falsified.

Recommended return: **Build Batch 6** (task-08 CLI Demo) as a prerequisite, followed by remaining pending tasks before closeout can be declared.
