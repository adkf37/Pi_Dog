# Task 10 — Voice Loop

**Phase:** 3 — Voice Loop
**Profile:** build
**Dependencies:** task-07, task-09
**Status:** pending

## Description

Add offline speech-to-text and text-to-speech to the robot loop. Implement wake word or keyboard-triggered voice capture. The voice loop lets the user speak a command, the LLM plan it, the robot execute actions, and TTS speak the response.

STT and TTS modules must work offline (no cloud dependency) and should be toggleable via `ENABLE_VOICE` config flag. Hardware-specific audio imports should be isolated similarly to PiDog hardware imports.

## Inputs

- Task 07 output (planner — `Planner.plan()`)
- Task 09 output (PiDog adapter)
- SunFounder voice chatbot tutorial (reference for offline voice stack on Pi)

## Outputs

- `src/pidog_brain/perception/voice_input.py` — wake word detection + keyboard-triggered capture
- `src/pidog_brain/speech/stt.py` — offline STT module (e.g. Vosk)
- `src/pidog_brain/speech/tts.py` — offline TTS module (e.g. Piper)
- `src/pidog_brain/speech/__init__.py`

## Acceptance Checks

- [ ] Wake word or keyboard key triggers voice capture in demo mode
- [ ] STT produces text prompt from recorded audio
- [ ] LLM processes prompt and TTS speaks the response aloud
- [ ] `ENABLE_VOICE=false` completely disables voice module imports
- [ ] Voice loop works in mock mode (STT/TTS stubs or print-based)
- [ ] Unit tests for STT/TTS interfaces with mock audio
