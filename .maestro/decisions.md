# Decision Log — PiDog Local LLM Brain

## 2026-07-01 — Initial Planning

### Decision 001: Maestro agent slate
- **Context:** Need to select minimal useful agent profiles for a `local_llm` project.
- **Decision:** Use planner, build, validator, scribe. No critic, MLE, or data engineer needed.
- **Rationale:** Project is a Python framework with well-defined SDK dependencies, not a data science / ML training effort. All data sources are public and documented.

### Decision 002: LLM backend abstraction
- **Context:** SunFounder examples use Ollama, but llama.cpp may offer better performance on Pi 5 8GB.
- **Decision:** Support both via an abstract `LLMBase` class; Ollama is the default first backend.
- **Rationale:** Abstraction cost is low (2 client files + base class) and lets us benchmark both paths without refactoring.

### Decision 003: Mock mode first
- **Context:** Hardware dependency slows development.
- **Decision:** All core logic (config, schema, policy, planner) must work with `--mode mock` on any laptop. PiDog imports are isolated to one adapter file.
- **Rationale:** Enables rapid iteration without Pi hardware; matches project_overview.md safety rule #10.

### Decision 004: Action vocabulary must be explicit and enum-constrained
- **Context:** LLM output must be safe; freeform text is dangerous.
- **Decision:** Actions are defined in a Pydantic enum, not inferred from strings. Policy layer rejects anything outside the enum.
- **Rationale:** Safety rule #1 (allow-list) and #2 (schema validation).

### Decision 005: Bench mode disables all movement

- **Context:** Robot should be safe to test on a workbench without falling.
- **Decision:** `BENCH_MODE=true` (default) sets `movement_enabled=False`, which blocks `step_forward`, `step_backward`, `turn_left`, `turn_right` in the policy layer.
- **Rationale:** Prevents accidents during development.

---

## 2026-07-01 — Task Review

### Decision 006: Split task-10 into voice (10) and sensors (11)
- **Context:** Original task-10 combined two milestones (Phase 3 Voice, Phase 4 Sensors) into one task. These are distinct features with different implementation surfaces.
- **Decision:** Split into task-10 (Voice Loop — STT, TTS, wake word) and task-11 (Sensor Reactions — touch, ultrasonic, event loop).
- **Rationale:** Each is independently testable. Voice can work without sensors and vice versa. Two bounded tasks are easier to schedule, validate, and debug than one combined task.

### Decision 007: Add task-12 for demo & polish closeout
- **Context:** Phase 5 (Demo & Polish) had no corresponding task file. The phases.md referenced it but the backlog/tasks/ didn't cover it.
- **Decision:** Create task-12 covering demo scripts, model benchmarks, documentation refresh, and final integration.
- **Rationale:** Without an explicit closeout task, the project would have no defined end state or handoff artifact.

## 2026-07-01 — Build Batch 1–3 (tasks 01–05)

### Decision 008: pydantic-settings for config
- **Context:** Need env-var-driven config with defaults and type coercion.
- **Decision:** Use `pydantic-settings` (pydantic v2 `BaseSettings`).
- **Rationale:** Idiomatic pattern, auto-reads `.env`, built-in type coercion; avoids hand-parsing env vars.

### Decision 009: Policy clamps durations, does not reject
- **Context:** LLM may produce durations exceeding `MAX_ACTION_DURATION_S`.
- **Decision:** Policy **clamps** overlong durations to the max, rather than rejecting the whole plan.
- **Rationale:** More resilient to LLM variation; the robot still does the intended action, just for the configured max duration.

### Decision 010: Mock robot uses `time.sleep(0.1)` per action
- **Context:** Need visual pacing when watching mock output.
- **Decision:** Insert a small 100ms sleep per action in mock mode.
- **Rationale:** Makes demo output readable without real hardware; short enough not to slow tests measurably.

## 2026-07-01 — Build Batch 4 (task-06 Ollama Client)

### Decision 011: OllamaClient raises typed exceptions instead of generic
- **Context:** Callers need to distinguish connection errors from timeouts from bad responses.
- **Decision:** Use `ConnectionError`, `TimeoutError`, and `RuntimeError` for distinct failure modes.
- **Rationale:** Lets callers (planner, CLI) handle each case differently (e.g., retry on timeout, abort on connection failure).

### Decision 012: LlamaCppClient is a stub for now
- **Context:** Task-06 spec says the file should be a stub raising `NotImplementedError`.
- **Decision:** Reduced the existing full implementation to a clear stub.
- **Rationale:** Ollama is the primary backend for v1; llama.cpp support can be completed when benchmarked and prioritized.

### Decision 013: Use `respx` for HTTP mocking in tests
- **Context:** Need to test OllamaClient HTTP calls without a real Ollama server.
- **Decision:** Added `respx` to test dependencies for in-process HTTP request mocking.
- **Rationale:** Lightweight, pytest-native, intercepts real httpx calls at the transport layer.

## 2026-07-04 — Build Batch 5 (task-07 Planner)

### Decision 014: Planner uses `LLMBase` abstraction, not concrete client
- **Context:** Planner needs to call an LLM but should not depend on Ollama or llama.cpp directly.
- **Decision:** Planner accepts any `LLMBase` instance via constructor injection.
- **Rationale:** Keeps the planner testable with mock LLMs; aligns with Decision 002 LLM backend abstraction.

### Decision 015: Parser extracts JSON from text via brace matching, not regex-only
- **Context:** LLM responses may contain markdown fences, surrounding text, or other non-JSON content.
- **Decision:** `parse_llm_response` first strips code fences, then finds the outermost `{...}` pair via brace-depth tracking.
- **Rationale:** More robust than regex for nested objects; handles fence variations (```, ```json) with or without language tag.

### Decision 016: Planner returns fallback `RobotPlan` with apology text on failure
- **Context:** LLM might fail (exception, invalid JSON, policy violation). The planner should never crash.
- **Decision:** Three fallback paths — LLM exception → "couldn't reach my planning engine"; parse failure → "couldn't understand"; policy violation → "planned something unsafe".
- **Rationale:** Graceful degradation; each failure mode has a distinct message for debugging; caller always gets a valid `RobotPlan`.

### Decision 017: `prompts.py` imports action descriptions from `robot/actions.py`
- **Context:** Prompt must include human-readable action descriptions for the LLM to pick appropriate actions.
- **Decision:** Reuse `ACTION_DESCRIPTIONS` dict from `robot/actions.py` rather than duplicating descriptions.
- **Rationale:** Single source of truth for action metadata; any future description changes propagate automatically to prompts.

---

## 2026-07-09 — Build Batch 6 (task-08 CLI Demo)

### Decision 019: main.py uses direct composition, not dependency injection framework
- **Context:** CLI entry point needs to wire up config → LLM → Planner → Robot.
- **Decision:** Use simple factory functions (`_build_llm`, `_build_robot`) rather than a DI framework.
- **Rationale:** The wiring is simple (4 components with 2 decision points). A DI framework adds complexity with no benefit for a single-entry-point CLI.

### Decision 020: `--bench` flag overrides config to force movement disabled
- **Context:** Settings default `bench_mode=True` for safety. The `--bench` flag should make bench mode explicit.
- **Decision:** `--bench` sets `settings.bench_mode = True`. Users can still enable movement via `BENCH_MODE=false` env var.
- **Rationale:** Explicit CLI flag is safer than silently relying on env default. Running `--bench` always means "disable movement" regardless of env state.

### Decision 021: Empty `--input` defaults to "say hello"
- **Context:** The acceptance check requires `--input "hello"`, but users may omit `--input`.
- **Decision:** If `--input` is empty string or omitted, default to `"say hello"`.
- **Rationale:** Provides a sensible demo behavior without requiring the user to always pass `--input`.

### Decision 022: Ruff added for lint, but type-checking deferred
- **Context:** Feedback requested lint/type-check infrastructure (ruff/mypy).
- **Decision:** Added ruff configuration (E, F, I, W rules) to `pyproject.toml`. No mypy/type-checking added.
- **Rationale:** Ruff is zero-config for basic lint and catches real issues. Full type-checking with mypy would require extensive annotation work across the codebase and is better as a separate task.

---

## 2026-07-04 — Validation (tasks 06–07)

### Decision 018: Validation passed — tasks 06–07 meet acceptance criteria
- **Context:** Build batches 4–5 produced OllamaClient (task-06) and Planner (task-07). Validator ran all 46 tests and reviewed implementation against acceptance criteria.
- **Evidence:**
  - Task 06: All 4 acceptance checks pass. 8 unit tests with respx-mocked HTTP covering success, payload shape, extra kwargs, connection error, timeout, HTTP error, and bad JSON.
  - Task 07: All 4 acceptance checks pass. 17 unit tests covering valid/invalid/malformed LLM responses, policy violations, prompt construction with/without robot state, parser edge cases (markdown fences, partial JSON, empty, garbage).
  - 46/46 tests pass. All imports resolve. Source code quality: clean separation of concerns, typed exceptions, constructor injection, brace-depth JSON parser, graceful fallback plans.
- **Outcome:** Pass. Recommend proceeding to Build Batch 6 (task-08 CLI Demo).
