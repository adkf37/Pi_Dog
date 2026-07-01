# Project Overview: PiDog Local LLM Brain on Raspberry Pi 5

## 1. Project Name

**pidog-local-brain**

## 2. One-Sentence Summary

Scaffold a Python repo for a Raspberry Pi 5 8GB project that runs a lightweight local LLM on-device and uses it as the high-level decision-making “brain” for a SunFounder PiDog robot dog.

## 3. Primary Goal

Build a clean, testable repo that lets Maestro develop the project in stages:

1. Bring up PiDog hardware on a Raspberry Pi 5.
2. Run a small local LLM on the Pi.
3. Convert natural-language prompts into safe, validated PiDog actions.
4. Add voice input/output and sensor-triggered behaviors after the text-control loop works.

The core deliverable is not a one-off demo script. It is a reusable local-robotics framework with clear boundaries between the LLM, action planning, hardware control, speech, sensors, configuration, and tests.

## 4. Hardware Target

### Required

- Raspberry Pi 5, 8GB RAM
- SunFounder PiDog **V2** robot dog kit
- microSD card or SSD boot drive
- Official-quality USB-C power for the Pi
- PiDog battery and Robot HAT setup per SunFounder instructions
- Keyboard/monitor or SSH access for initial setup

### Important Compatibility Note

Use the **PiDog V2** kit for Raspberry Pi 5. SunFounder’s documentation says the Standard version is not suitable for Raspberry Pi 5 because its servo motors and Robot HAT are not compatible, while V2 adds Raspberry Pi 5 support through updated servo drivers and HAT circuitry.

## 5. Source Facts to Preserve

- PiDog includes 12 metal gear servos, a camera module, ultrasonic obstacle sensing, touch sensors, sound direction sensing, a 6-DOF IMU, a light board, speaker support, and dog-like actions such as walking, standing, sitting, head movement, and posing.
- SunFounder provides Python libraries and examples through the `pidog`, `robot-hat`, and `vilib` repos/modules.
- SunFounder’s AI examples include local Ollama-based text chat, local voice chatbot flows using STT + local LLM + TTS, and action keywords mapped into robot motions.
- Raspberry Pi 5 8GB can run small quantized LLMs, but memory and latency will be tight. Start with small models and keep the robot action loop asynchronous from model generation.

## 6. Non-Goals for the First Version

- Do not attempt autonomous navigation.
- Do not attempt real-time visual reasoning from the camera in v1.
- Do not let the LLM directly generate arbitrary Python or servo commands.
- Do not depend on cloud LLMs for the core demo.
- Do not build a polished mobile app.
- Do not optimize for maximum model quality at the expense of stability.

## 7. Recommended Technical Direction

### Runtime Strategy

Start with an abstraction layer that supports two local LLM backends:

1. **Ollama backend** — easiest first integration because SunFounder’s PiDog examples already include Ollama-based flows.
2. **llama.cpp backend** — useful fallback for more direct GGUF control, potentially less overhead, and easier benchmarking of tiny models.

Default for first demo: **Ollama local on the Pi** using a small model.

Stretch path: switch to `llama.cpp` / `llama-cpp-python` if Ollama is too slow or memory-heavy on the 8GB Pi.

### Model Candidates

Treat model selection as an experiment. The repo should make this configurable.

Starter candidates:

- `tinyllama` / 1B-class model for first bootstrapping
- `moondream:1.8b` or another small model if available and relevant
- `phi3:mini` as a possible text model if latency is acceptable
- `llama3.2:3b` only as a stretch test on the 8GB Pi; SunFounder’s own table treats ~3B as requiring 8GB minimum, with 16GB preferred

The first working demo should prioritize reliable action selection over conversational quality.

## 8. Core Architecture

```text
User input / sensors
        |
        v
Input normalizer
        |
        v
LLM planner  ---> prompt templates + robot persona + action schema
        |
        v
Action parser / validator
        |
        v
Safety policy / rate limiter / allow-list
        |
        v
Robot adapter
        |
        v
PiDog Python library / mock robot
```

### Key Principle

The LLM chooses from a small, explicit action vocabulary. It never controls servos directly.

Example LLM output contract:

```json
{
  "say": "Sure. I’ll do a happy little stretch.",
  "actions": [
    {"name": "stand", "duration_s": 1.0},
    {"name": "wag_tail", "duration_s": 2.0},
    {"name": "sit", "duration_s": 1.0}
  ]
}
```

The code should reject anything outside the allowed schema.

## 9. Initial Action Vocabulary

Start small:

- `sit`
- `stand`
- `rest`
- `nod`
- `shake_head`
- `wag_tail`
- `bark`
- `howl`
- `stretch`
- `step_forward`
- `step_backward`
- `turn_left`
- `turn_right`
- `stop`

Each action should map to one safe method in the PiDog adapter. Movement actions should have conservative default durations and should be disabled when the robot is in “bench mode.”

## 10. Repo Scaffold

```text
pidog-local-brain/
  README.md
  project_overview.md
  pyproject.toml
  .env.example
  .gitignore

  src/
    pidog_brain/
      __init__.py
      main.py
      config.py

      llm/
        __init__.py
        base.py
        ollama_client.py
        llama_cpp_client.py

      planner/
        __init__.py
        prompts.py
        schema.py
        parser.py
        policy.py

      robot/
        __init__.py
        base.py
        mock_robot.py
        pidog_adapter.py
        actions.py

      perception/
        __init__.py
        sensors.py
        keyboard_input.py
        voice_input.py

      speech/
        __init__.py
        stt.py
        tts.py

      runtime/
        __init__.py
        event_loop.py
        logging.py
        telemetry.py

  scripts/
    setup_pi.sh
    install_sunfounder_stack.sh
    install_ollama.sh
    pull_model.sh
    run_text_demo.sh
    run_robot_demo.sh
    run_voice_demo.sh

  tests/
    test_action_schema.py
    test_parser.py
    test_policy.py
    test_mock_robot.py

  docs/
    hardware_setup.md
    model_benchmarks.md
    action_vocabulary.md
    demo_plan.md
```

## 11. Key Files Maestro Should Create First

### `README.md`

Include:

- What the project does
- Hardware/software requirements
- Quick start for mock mode
- Quick start for PiDog mode
- Safety notes for using physical servos
- Model configuration examples

### `pyproject.toml`

Use a simple Python package layout. Suggested dependencies:

- `pydantic` for action schemas
- `requests` or `httpx` for Ollama API calls
- `python-dotenv` for configuration
- `pytest` for tests
- optional: `llama-cpp-python`

Do not make `pidog` a hard dependency for development on a laptop. The repo should run in mock mode without robot hardware.

### `.env.example`

```bash
PIDOG_MODE=mock
LLM_BACKEND=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=tinyllama
BENCH_MODE=true
MAX_ACTIONS_PER_TURN=3
MAX_ACTION_DURATION_S=3
ENABLE_VOICE=false
ENABLE_CAMERA=false
```

### `planner/schema.py`

Define the only valid LLM response shape.

### `planner/policy.py`

Reject invalid, unsafe, too-long, or unsupported actions.

### `robot/mock_robot.py`

Print actions to the console for development without hardware.

### `robot/pidog_adapter.py`

Wrap the SunFounder `Pidog` library. This should be the only place that imports PiDog-specific hardware libraries.

## 12. Development Milestones

### Milestone 0 — Repo Scaffolding

Acceptance criteria:

- Repo installs locally in editable mode.
- `pytest` passes.
- `python -m pidog_brain.main --mode mock` runs without PiDog hardware.
- Mock mode prints validated actions.

### Milestone 1 — PiDog Hardware Bring-Up

Acceptance criteria:

- Raspberry Pi OS 64-bit is installed.
- SunFounder `robot-hat`, `vilib`, and `pidog` modules are installed.
- PiDog calibration is complete.
- Simple PiDog actions work outside this repo using official examples.
- This repo can run one allow-listed hardware action, such as `sit` or `wag_tail`.

### Milestone 2 — Local LLM Text Demo

Acceptance criteria:

- Local LLM runs on the Pi.
- Prompt returns valid JSON matching the schema at least 80% of the time.
- Invalid JSON is retried or safely ignored.
- Demo command works:

```bash
python -m pidog_brain.main --mode mock --input "act excited when I come home"
```

Expected behavior:

- The LLM produces a short phrase and 1–3 safe actions.
- Mock robot logs the actions.

### Milestone 3 — LLM-to-PiDog Action Bridge

Acceptance criteria:

- Same prompt can trigger real PiDog actions.
- Robot always returns to a stable posture after an action sequence.
- `stop` can interrupt an action sequence.
- Movement actions are disabled unless explicitly enabled.

### Milestone 4 — Voice Loop

Acceptance criteria:

- Wake word or keyboard-triggered voice capture works.
- Speech-to-text produces a prompt.
- LLM produces a validated response.
- Text-to-speech speaks the response.
- PiDog executes actions after speech or in parallel where appropriate.

### Milestone 5 — Sensor Reactions

Acceptance criteria:

- Touch sensor can trigger “happy” or “avoid” behavior.
- Ultrasonic sensor can trigger a safe back-up or stop behavior.
- Sensor events bypass or constrain the LLM when speed matters.
- LLM can add personality only after the safety action is chosen.

### Milestone 6 — Demo Script

Acceptance criteria:

- One command starts the demo.
- The demo supports mock mode and robot mode.
- The demo includes 5–8 scripted prompts.
- Logs include model name, response latency, parse success/failure, and executed actions.

## 13. Safety and Reliability Rules

1. Use an action allow-list.
2. Validate every LLM response against a schema.
3. Cap action sequence length.
4. Cap each action duration.
5. Keep movement conservative by default.
6. Add a stop interrupt.
7. Return to stable posture after each sequence.
8. Do not run untrusted generated code.
9. Keep hardware-specific imports isolated.
10. Support mock mode for most development.

## 14. Prompting Strategy

Use a strict system prompt:

```text
You are the planning brain for a small Raspberry Pi robot dog.
You must respond only with JSON matching the provided schema.
You may choose only from the allowed action list.
Do not invent actions.
Do not describe servo angles.
Do not write code.
Keep action sequences short and safe.
```

Add runtime context:

```text
Robot state:
- mode: bench | floor
- battery: unknown | low | ok
- obstacle_distance_cm: null or number
- touch_event: none | front | rear | front_to_rear | rear_to_front
- movement_enabled: true | false
```

## 15. Testing Plan

### Unit Tests

- Valid JSON parses into action schema.
- Invalid actions are rejected.
- Too many actions are rejected.
- Long durations are clamped or rejected.
- Movement is blocked in bench mode.
- Mock robot records expected calls.

### Integration Tests

- Mock LLM → planner → mock robot.
- Ollama → planner → mock robot.
- Ollama → planner → PiDog adapter.

### Hardware Smoke Tests

- `sit`
- `stand`
- `wag_tail`
- `nod`
- `stop`

Run hardware smoke tests before any walking behavior.

## 16. Model Benchmark Log

Create `docs/model_benchmarks.md` with this table:

| Model | Backend | Quantization | RAM Used | Tokens/sec | First Token Latency | JSON Reliability | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| TBD | Ollama | TBD | TBD | TBD | TBD | TBD | TBD |

Benchmark with:

1. Simple chat prompt.
2. Action-selection prompt.
3. Prompt with sensor context.
4. Prompt that tries to make the model invent an unsupported action.

## 17. Initial Maestro Task Packet

### Task 1 — Scaffold Repo

Create the repo structure above with a Python package under `src/pidog_brain`.

### Task 2 — Implement Config

Read settings from environment variables with sane defaults. Support `mock` and `robot` modes.

### Task 3 — Implement Action Schema

Use Pydantic models for:

- `RobotPlan`
- `RobotAction`
- allowed action enum

### Task 4 — Implement Policy Layer

Validate and sanitize every plan before execution.

### Task 5 — Implement Mock Robot

The mock robot should log action calls and return a structured result.

### Task 6 — Implement Ollama Client

Call the local Ollama API and return text. Keep this independent of PiDog hardware.

### Task 7 — Implement Planner

Build prompt, call LLM, parse JSON, validate policy, and return a safe plan.

### Task 8 — Implement CLI Demo

Add CLI entry points:

```bash
python -m pidog_brain.main --mode mock --input "say hello and wag your tail"
python -m pidog_brain.main --mode robot --input "sit and look happy"
```

### Task 9 — Implement PiDog Adapter

Wrap official PiDog methods behind the repo’s action vocabulary.

### Task 10 — Add Hardware Setup Docs

Create `docs/hardware_setup.md` with steps for Pi OS, SunFounder libraries, calibration, and smoke tests.

## 18. First Working Demo Definition

The first demo is text-only:

```bash
python -m pidog_brain.main --mode robot --input "act excited to see me, but stay in place"
```

Expected behavior:

1. LLM returns valid JSON.
2. Policy allows only non-walking actions.
3. PiDog says or prints a short response.
4. PiDog performs a short safe action sequence, such as wag tail, nod, sit.
5. PiDog returns to a stable posture.

## 19. Stretch Features

- Voice wake word
- Offline Vosk STT
- Piper TTS
- Camera snapshot description through a tiny vision model or remote optional model
- Personality profiles: shy, playful, guard dog, sleepy puppy
- Kid-safe command mode
- Web dashboard for prompts, logs, and action debugging
- OpenClaw adapter as an optional integration layer

## 20. Biggest Risks

### Risk 1 — Pi 5 8GB LLM performance is too slow

Mitigation:

- Start with 1B-class or smaller models.
- Use short prompts.
- Use constrained JSON output.
- Keep common behaviors rule-based.
- Make larger models optional over LAN.

### Risk 2 — Power instability with servos and Pi 5

Mitigation:

- Confirm V2 kit.
- Use conservative actions first.
- Avoid walking until simple stationary actions are stable.
- Log undervoltage or shutdown symptoms.

### Risk 3 — LLM generates unsafe or unsupported actions

Mitigation:

- Strict schema.
- Allow-list.
- Policy layer.
- Movement disabled by default.
- Stop interrupt.

### Risk 4 — Hardware dependency slows development

Mitigation:

- Mock mode must work on any laptop.
- PiDog imports isolated to `pidog_adapter.py`.
- Unit tests should not require robot hardware.

## 21. Recommended First Commit

Commit message:

```text
Initial scaffold for PiDog local LLM brain
```

Files included:

- `README.md`
- `project_overview.md`
- `pyproject.toml`
- `.env.example`
- `src/pidog_brain/...`
- `tests/...`
- `docs/hardware_setup.md`

## 22. References

- SunFounder PiDog documentation: https://docs.sunfounder.com/projects/pidog/en/latest/
- SunFounder PiDog GitHub repo: https://github.com/sunfounder/pidog
- SunFounder PiDog local Ollama tutorial: https://docs.sunfounder.com/projects/pidog/en/latest/ai_interaction/python_llm_ollama.html
- SunFounder PiDog local voice chatbot tutorial: https://docs.sunfounder.com/projects/pidog/en/latest/ai_interaction/python_local_chatbot.html
- Arm Learning Path: local LLM chatbot on Raspberry Pi 5: https://learn.arm.com/learning-paths/embedded-and-microcontrollers/llama-python-cpu/llama-python-chatbot/
