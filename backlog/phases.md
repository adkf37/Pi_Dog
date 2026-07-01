# Phases — PiDog Local LLM Brain

## Phase 0: Scaffolding (Build)

- Create Python package structure under `src/pidog_brain/`
- `pyproject.toml`, `README.md`, `.env.example`, `.gitignore`
- Mock robot, config, schema, policy, tests
- **Acceptance:** `pip install -e .` works, `pytest` passes, mock demo runs

## Phase 1: LLM Integration (Build)

- Implement Ollama client and LlamaCpp client
- Implement planner (prompt builder → LLM call → JSON parser → policy)
- Implement CLI demo entry point
- **Acceptance:** LLM returns valid JSON matching schema >=80% of the time; policy rejects bad output

## Phase 2: Hardware Bridge (Build)

- PiDog hardware bring-up on Raspberry Pi 5
- `pidog_adapter.py` wrapping SunFounder library
- Hardware smoke tests (sit, stand, wag_tail)
- **Acceptance:** Repo drives real PiDog actions through the adapter

## Phase 3: Voice Loop (Build)

- Speech-to-text integration (Vosk or similar offline STT)
- Text-to-speech integration (Piper or similar offline TTS)
- Wake word or keyboard-triggered voice capture
- **Acceptance:** Full voice-in → LLM → voice-out + action loop works on Pi

## Phase 4: Sensor Reactions (Build)

- Touch sensor → trigger behavior
- Ultrasonic sensor → safe stop/backup
- Sensor events bypass LLM when speed matters
- **Acceptance:** Sensor-triggered actions fire without LLM latency

## Phase 5: Demo & Polish (Validate + Closeout)

- One-command demo script
- 5–8 scripted prompts
- Model benchmark log (`docs/model_benchmarks.md`)
- Logging, telemetry, docs refresh
- **Acceptance:** Demo runs end-to-end in mock and hardware modes
