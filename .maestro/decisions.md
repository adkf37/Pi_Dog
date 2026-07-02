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
