# PiDog Local LLM Brain

## Objective

Build a Python framework that runs a lightweight local LLM on a Raspberry Pi 5 (8GB) and uses it as the high-level decision-making "brain" for a SunFounder PiDog V2 robot dog.

The LLM selects from a constrained vocabulary of safe robot actions; it never controls servos directly. The core deliverable is a reusable local-robotics framework with clear boundaries between the LLM, action planning, hardware control, speech, sensors, configuration, and tests.

## Success Criteria

1. Repo installs via `pip install -e .` and passes `pytest` without PiDog hardware.
2. `python -m pidog_brain.main --mode mock --input "say hello"` runs on any laptop and prints validated actions.
3. An Ollama-backed LLM on the Pi produces valid JSON (matching the action schema) at least 80% of the time.
4. The same prompt can drive real PiDog hardware actions (sit, stand, wag_tail, etc.) through the `pidog_adapter.py` module.
5. Action safety policy rejects invalid actions, caps sequence length and duration, and blocks movement in bench mode.
6. Voice input/output (STT + TTS) and sensor-triggered behaviors work as stretch milestones.

## Non-Goals (v1)

- No autonomous navigation.
- No real-time visual reasoning from camera.
- No cloud LLM dependency for the core demo.
- No direct LLM-generated Python or servo commands.
- No polished mobile app.

## Project Type

local_llm — priority: medium
