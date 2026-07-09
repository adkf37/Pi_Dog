# Critic Report — Pi_Dog

| Field | Value |
|---|---|
| Date | 2026-07-09 |
| Agent | critic |
| Checkpoint | after-first-build-merge |
| Return Phase | validate |

## Commands / Checks Attempted

```bash
pip install -e .                       # OK — installs successfully
python -m pytest tests/ -v             # 55/55 passed (6.60s)
python -c "import pidog_brain"         # OK
python -m pidog_brain.main --mode mock --input "hello"   # Runs, fallback plan (no Ollama)
python -m pidog_brain.main --mode mock --bench --input "hello"  # Bench mode confirmed
python -m pidog_brain.main --mode robot --input "hello"  # Silently falls back to MockRobot
ruff check src/                        # Not installed in environment
```

## Previous Critic Findings — Re-assessment

| # | Severity | Finding (2026-07-04) | Current Status | Notes |
|---|---|---|---|---|
| 1 | Block | Phase mismatch (closeout vs build) | **Addressed** — phase corrected to `build` |
| 2 | Block | CLI demo skeleton does not wire planner/robot | **Addressed** — `main.py` now wires config → LLM → Planner → MockRobot; 9 CLI tests added |
| 3 | Block | SC3 (80% valid JSON) not measurable | **Wontfix** — rationale accepted; real-Ollama benchmarking deferred to hardware bring-up |
| 4 | Warn | OllamaClient tested only with mocked HTTP | **Wontfix** — rationale accepted; real-hardware smoke testing deferred |
| 5 | Warn | No lint/type-check infrastructure | **Addressed** — ruff configured in `pyproject.toml` (E, F, I, W rules) |
| 6 | Warn | Empty subpackages misrepresent progress | **Wontfix** — rationale accepted; intentional stubs for pending tasks |

All three previous blocking issues have been addressed or accepted. The project has advanced from 46 to 55 tests and from 7 to 8 completed tasks since the last critic review.

## New Adversarial Findings

### Finding 1 (WARN) — `--mode mock` still tries real Ollama connection

The `--mode mock` flag suggests an entirely mocked pipeline, but the LLM backend is always `ollama` by default. Without a running Ollama server, the demo produces 0 actions and an apology message — it demonstrates the *error path*, not the *planning pipeline*. A user running `python -m pidog_brain.main --mode mock --input "say hello"` on a laptop sees:

```
Actions:      0
Speech:       I'm sorry, I couldn't reach my planning engine.
```

This fails the spirit of SC2 ("prints validated actions"). In mock mode, the system should use a `MockLLM` (or similar) so the demo actually demonstrates action planning, not just graceful fallback.

**Evidence:**
- `src/pidog_brain/main.py:19-28` — `_build_llm` returns `OllamaClient` or `LlamaCppClient`; never a mock LLM
- `backlog/README.md:12` — SC2: "prints validated actions"
- `backlog/tasks/task-08-cli-demo.md:24` — Acceptance: "prints validated actions"
- Terminal output (verified above): fallback plan with 0 actions

**Linked Tasks:** task-08

---

### Finding 2 (WARN) — Prompt constraints hardcoded, not derived from config

The prompt builder in `planner/prompts.py` hardcodes constraints:
- `" - 'duration_s' must be a positive number (max 3.0)"`
- `"  - Maximum 3 actions per response"`

These values come from `MAX_ACTION_DURATION_S` (3.0) and `MAX_ACTIONS_PER_TURN` (3) in config, but the prompt does not read config at all. If a user changes these settings (e.g. allowing 5 actions), the prompt tells the LLM a different limit, and the planner silently overrides the LLM's output. The user gets no indication that the LLM was asked to follow different rules than the policy enforces.

**Evidence:**
- `src/pidog_brain/planner/prompts.py:34-37` — Hardcoded "max 3.0" and "Maximum 3 actions"
- `src/pidog_brain/planner/prompts.py` — No import of config or Settings
- Reproduction: change `MAX_ACTIONS_PER_TURN=5` in `.env`; prompt still says "Maximum 3 actions"

**Linked Tasks:** task-07

---

### Finding 3 (WARN) — `--mode robot` silently ignored

The `_build_robot` function always returns a `MockRobot`, regardless of mode. It logs a WARNING about task-09 not being implemented, but the output summary still says `Mode: robot`. A user running `--mode robot` sees identical behavior to `--mode mock` and may believe the PiDog adapter is active.

The acceptance check for task-08 says "safe to fail if no hardware," which is reasonable, but the silent fallback is misleading. At minimum, `_build_robot("robot")` should attempt to import and instantiate `PiDogAdapter` (with a try/except for `ImportError`) before falling back.

**Evidence:**
- `src/pidog_brain/main.py:32-38` — `_build_robot` always returns `MockRobot` for any mode
- `backlog/tasks/task-08-cli-demo.md:25` — Acceptance: "`--mode robot` selects the real PiDog adapter (safe to fail if no hardware)"
- The current implementation does not even attempt PiDogAdapter import

**Linked Tasks:** task-08, task-09

---

### Finding 4 (WARN) — No validation report exists for task-08

The previous validation report (`.maestro/validation_report.md`) covers tasks 06–07 only. Task-08 (CLI Demo) was built as Build Batch 6 but has never been formally validated against its acceptance criteria by a validator agent. While the builder tests pass, there is no recorded evidence that a validator reviewed:
- `python -m pidog_brain.main --mode mock --input "hello"` output
- `--mode robot` fallback behavior
- `--bench` flag correctness
- Log output format compliance

**Evidence:**
- `.maestro/validation_report.md:7-8` — Agent scope: "Build Batch(es) 4–5 (tasks 06–07)"
- No task-08 validation section exists in any `.maestro/` report

**Linked Tasks:** task-08

---

### Finding 5 (WARN) — Test coverage gaps in CLI

The `test_main.py` file covers the success path but leaves two branches untested:

1. **Planner exception path** (`main.py:108`): The `except Exception` block that catches planner errors is never exercised. Every test patches `Planner.plan` to return a valid `RobotPlan`.
2. **`plan is None` guard** (`main.py:115`): The branch handling a missing plan is not tested.
3. **`_build_robot("robot")` path** (`main.py:33-38`): The warning log for robot mode is not tested.

**Evidence:**
- `tests/test_main.py:62-82` — `test_main_runs_mock_mode` patches `Planner.plan` to return valid plan; never tests exception
- `tests/test_main.py` — No test for `--mode robot` or the warning log message
- `tests/test_main.py` — No test for `planner.plan()` raising an exception

**Linked Tasks:** task-08

---

### Finding 6 (WARN) — SC3 remains unmeasured and no plan exists to measure it

The previous critic identified SC3 (80% valid-JSON from Ollama) as an unmeasurable blocking issue. The builder marked it `wontfix` with rationale: "better treated as a hardware-validation step." As critic, I re-evaluate this:

The `wontfix` rationale is reasonable in theory, but as the project now has 8 of 12 tasks complete and is approaching hardware deployment, there is still **no plan, no script, and no measurement infrastructure** for validating SC3. The acceptance criterion remains in the backlog as a success criterion, but it has been effectively abandoned with no documented replacement.

At minimum, the project should either:
- Remove SC3 from the success criteria (and update `backlog/README.md`), or
- Add the measurement infrastructure as a sub-task of task-09 (PiDog Adapter) or task-12 (Demo & Polish)

**Evidence:**
- `backlog/README.md:13` — SC3 still present as a live success criterion
- `FEEDBACK.md:58-60` — Rationale: "hardware-validation step performed on the Pi"
- `.maestro/task_plan.md:89` — task-09 risk flag mentions "requires physical PiDog hardware to verify" (adapter) but not SC3 measurement

**Linked Tasks:** task-09, task-12

---

### Finding 7 (WARN) — Ruff configured but not installable as dev dependency

Ruff was added to `pyproject.toml` (Finding 5 resolution from previous critic), but it is not listed in any dependency group. Running `ruff check src/` fails with "No module named ruff" unless the user explicitly `pip install ruff`. There is no `pre-commit` hook, no `nox` session, and no CI config to run it. The ruff configuration exists but is inert in practice.

**Evidence:**
- `pyproject.toml:21-29` — Ruff configuration present
- `pyproject.toml:16-17` — Only optional-dependencies: `llama` extra; no `dev` or `lint` extra
- `requirements.txt` — No ruff listed
- Verified: `ruff check src/` fails with module-not-found

**Linked Tasks:** task-01

## Verdict

**Warn** — The project has made substantial progress: 8 of 12 tasks complete, 55/55 tests passing, CLI wired end-to-end, previous blocking issues addressed. The architecture and code quality remain clean. However, seven residual concerns should be addressed before closeout:

1. Mock mode should demonstrate the planning pipeline, not just the error path.
2. Prompt constraints should derive from config to avoid misleading the LLM.
3. `--mode robot` should attempt PiDogAdapter import before falling back.
4. Task-08 requires formal validation.
5. CLI test coverage has untested exception paths.
6. SC3 needs either measurement infrastructure or removal from acceptance criteria.
7. Ruff configuration is inert without a dev-dependency or CI integration.

The project should return to **validate** for formal task-08 validation, then continue build for tasks 09–12.
