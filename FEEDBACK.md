# FEEDBACK - Pi_Dog

> Drop feedback here for the next Maestro worker to pick up.
> The assigned agent reads this file at the start of each work cycle.
> Maestro parses this file: every entry with `Status: open` (or `in-progress`)
> blocks closeout from declaring `Complete` and is injected into the next
> dispatch prompt.

## Format

```
### YYYY-MM-DD - [Your Name or "Human"]
Status: open
Priority: [high | medium | low]
Scope: [direction | code | data | priority]
Linked Tasks: [task-12, task-15]  # optional

[Your feedback here]
```

Status values:
- `open` — not yet acted on (default if `Status:` omitted)
- `in-progress` — agent is working on it; still blocks Complete
- `addressed` — done; PR/commit reference in body
- `wontfix` — intentionally skipped; body must explain why

## Feedback Log

### 2026-07-04 - Critic
Status: open
Priority: high
Scope: critic
Severity: block
Linked Tasks: task-08, task-09, task-10, task-11, task-12

**Phase mismatch:** STATUS.md claims `Phase: closeout` but only tasks 01–07 are complete. Tasks 08–12 (CLI Demo, PiDog Adapter, Voice Loop, Sensor Reactions, Demo & Polish) are all `pending`. The STATUS.md `Next Action` ("Proceed to Build Batch 6") contradicts the closeout phase. Reset STATUS.md phase to `build` and complete pending tasks before closeout.

### 2026-07-04 - Critic
Status: open
Priority: high
Scope: critic
Severity: block
Linked Tasks: task-08

**Success Criterion 2 fails:** `python -m pidog_brain.main --mode mock --input "hello"` does not produce validated actions. `src/pidog_brain/main.py` is a skeleton that only prints configuration. Implement task-08 to wire config → planner → mock robot before closeout.

### 2026-07-04 - Critic
Status: open
Priority: high
Scope: critic
Severity: block
Linked Tasks: task-07, task-08

**Success Criterion 3 not measurable:** The 80% valid-JSON threshold from Ollama has no test, benchmark, or measurement infrastructure. All 17 planner tests use `MockLLM`. No prompt iteration or real Ollama endpoint testing has occurred. Adjust SC3 or build measurement infrastructure.

### 2026-07-04 - Critic
Status: open
Priority: medium
Scope: critic
Severity: warn
Linked Tasks: task-06

**OllamaClient acceptance tested only with mocked HTTP:** All 8 OllamaClient tests use `respx`-mocked HTTP. The client has never been verified against a real Ollama API instance. Address when real hardware is available.

### 2026-07-04 - Critic
Status: open
Priority: medium
Scope: critic
Severity: warn
Linked Tasks: task-01

**No lint/type-check infrastructure:** The repo has no configured linter or type checker. For headless Raspberry Pi deployment, type errors could cause runtime crashes. Add ruff/mypy configuration before hardware deployment.

### 2026-07-04 - Critic
Status: open
Priority: low
Scope: critic
Severity: warn
Linked Tasks: task-10, task-11

**Empty subpackages misrepresent progress:** `perception/`, `speech/`, `runtime/` contain only empty `__init__.py` files. These correspond to pending tasks 10/11. Structure is correct but could mislead about actual completion state.
