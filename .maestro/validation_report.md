# Validation Report — Pi_Dog

| Field | Value |
|---|---|
| Date | 2026-07-04 |
| Agent | validator |
| Build Batch(es) | 4–5 (tasks 06–07) |
| Tests Run | All 46 pytest tests |
| Lint/Type Checks | None configured in repo |

## Commands Run

```bash
pip install -e .                # Package installs successfully
pip install pytest respx         # Test dependencies
python -m pytest tests/ -v       # 46 passed, 0 failed
python -c "import pidog_brain"   # Import OK
```

## Task 06 — OllamaClient Acceptance

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `OllamaClient.generate(prompt)` returns response text | ✅ PASS | `test_ollama_client_generates_text` — respx-mocked HTTP returns "Hello world!" |
| 2 | Client reads host/model from config | ✅ PASS | `test_ollama_client_uses_config_host_and_model` — asserts config values propagate |
| 3 | Timeout / connection error handled gracefully | ✅ PASS | 4 tests: connection error → `ConnectionError`, timeout → `TimeoutError`, HTTP 503 → `RuntimeError`, bad JSON → `RuntimeError` |
| 4 | Unit tests with mocked HTTP responses | ✅ PASS | 8 tests using `respx_mock` — covers generate, payload shape, extra kwargs, and all error paths |

**Task 06 verdict: ✅ All acceptance checks pass**

## Task 07 — Planner Acceptance

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `Planner.plan(user_input, robot_state)` returns validated `RobotPlan` | ✅ PASS | `test_planner_returns_validated_plan` — valid JSON → correctly parsed `RobotPlan` with `AllowedAction.sit` |
| 2 | Invalid JSON returns safe fallback | ✅ PASS | `test_planner_invalid_json_fallback` — garbage input → `"couldn't understand"` fallback with empty actions |
| 3 | Policy violations caught before returning | ✅ PASS | `test_planner_policy_violation_fallback` — movement in bench mode → `"unsafe"` fallback |
| 4 | Unit tests with mock LLM | ✅ PASS | 14 tests covering: valid plan, invalid JSON, policy violation, LLM exception, user input in prompt, robot state in prompt, empty input, parser (valid JSON, markdown fences, no-lang fences, garbage, empty, partial JSON), prompt builder (action list, user input, robot state, no state) |

**Task 07 verdict: ✅ All acceptance checks pass**

## Additional Observations

- **Parser** (`planner/parser.py`): Uses brace-depth tracking for JSON extraction (Decision 015), handles markdown fences with/without language tag, partial JSON with surrounding text.
- **Planner** (`planner/__init__.py`): Constructor injection of `LLMBase` (Decision 014), three distinct fallback paths (Decision 016).
- **Prompts** (`planner/prompts.py`): Imports `ACTION_DESCRIPTIONS` from `robot/actions.py` (Decision 017) — single source of truth.
- **Policy** (`planner/policy.py`): Clamps durations instead of rejecting (Decision 009).
- **OllamaClient** (`llm/ollama_client.py`): Typed exceptions for distinct failure modes (Decision 011).
- **LlamaCppClient** (`llm/llama_cpp_client.py`): Clean stub raising `NotImplementedError` (Decision 012).
- **main.py**: Basic argparse skeleton exists (task-08 not yet wired — expected, task-08 is pending).

## Blocked Checks

- No lint/type-check infrastructure configured in repo. Not a blocker for this phase.
- No PiDog hardware available for hardware-dependent integration tests (expected per project design).

## Evidence

- Test output: `46 passed in 6.68s`
- Import verification: `import pidog_brain` and key submodules all succeed
- Source review: All acceptance criteria files present and functionally complete

## Verdict

**Pass** — Tasks 06–07 meet all acceptance criteria. Recommend advancing to Build Batch 6 (task-08 CLI Demo).
