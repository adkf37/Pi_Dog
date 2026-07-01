# Task 10 — Voice & Sensor Integration

**Phase:** 3–4 — Voice Loop / Sensor Reactions
**Profile:** build
**Dependencies:** task-07, task-09
**Status:** pending

## Description

Add speech-to-text (Vosk or offline STT), text-to-speech (Piper or offline TTS), and sensor-triggered behaviors (touch, ultrasonic). Sensor events bypass or constrain LLM when speed matters.

## Inputs

- Task 07 output (planner)
- Task 09 output (PiDog adapter)

## Outputs

- `src/pidog_brain/perception/voice_input.py` — wake word detection + STT capture
- `src/pidog_brain/speech/stt.py` — STT module
- `src/pidog_brain/speech/tts.py` — TTS module
- `src/pidog_brain/perception/sensors.py` — touch + ultrasonic sensor handlers
- `src/pidog_brain/runtime/event_loop.py` — main async event loop

## Acceptance Checks

- [ ] Wake word or keyboard key triggers voice capture in demo mode
- [ ] STT produces text prompt from audio
- [ ] LLM processes prompt and TTS speaks the response
- [ ] Touch sensor triggers a pre-defined behavior (happy / avoid)
- [ ] Ultrasonic sensor triggers safe stop / backup within 500ms
- [ ] Sensor events fire without waiting for LLM
