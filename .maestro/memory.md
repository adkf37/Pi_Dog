# Memory — PiDog Local LLM Brain

## Project Facts

- **Repo:** `adkf37/Pi_Dog` — GitHub
- **Hardware:** Raspberry Pi 5 8GB + SunFounder PiDog V2
- **Python package:** `pidog-brain` under `src/pidog_brain/`
- **Default LLM backend:** Ollama (local, tiny models like tinyllama or phi3:mini)
- **Fallback LLM backend:** llama.cpp (via `llama-cpp-python`)
- **Config mode defaults:** `PIDOG_MODE=mock`, `BENCH_MODE=true`, `MAX_ACTIONS_PER_TURN=3`, `MAX_ACTION_DURATION_S=3`
- **Action vocabulary:** 14 actions — sit, stand, rest, nod, shake_head, wag_tail, bark, howl, stretch, step_forward, step_backward, turn_left, turn_right, stop
- **Action safety:** schema validation → policy layer → execution; movement blocked in bench mode
- **Hardware isolation:** PiDog imports only in `pidog_adapter.py`
- **Branch naming:** `maestro/{phase}-{kebab-case-slug}`
- **Commit prefix:** `[Planner]`, `[Build]`, `[Validate]`, `[Closeout]`

## Key Constraints

- No cloud LLM dependency for core demo
- No direct LLM-generated Python or servo commands
- No autonomous navigation in v1
- Tests must run without PiDog hardware
- All movements conservative by default
