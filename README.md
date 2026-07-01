# PiDog Local LLM Brain

A Python framework that runs a lightweight local LLM on a Raspberry Pi 5 to serve as the high-level decision-making "brain" for a SunFounder PiDog V2 robot dog.

## Hardware / Software Requirements

- Raspberry Pi 5, 8GB RAM
- SunFounder PiDog V2 robot dog kit
- Python 3.10+
- Ollama (recommended) or llama.cpp for local LLM inference

## Quick Start — Mock Mode (any laptop)

```bash
pip install -e .
python -m pidog_brain.main --mode mock --input "say hello and wag your tail"
```

## Quick Start — PiDog Mode

```bash
pip install -e .
# On Raspberry Pi with PiDog hardware attached:
python -m pidog_brain.main --mode robot --input "sit and look happy"
```

## Safety Notes

- Movement actions (`step_forward`, `step_backward`, `turn_left`, `turn_right`) are **disabled by default** (bench mode).
- Set `BENCH_MODE=false` in `.env` or environment to enable movement.
- The LLM never controls servos directly; it selects from a predefined action vocabulary.
- All actions are validated against a schema and safety policy before execution.

## Configuration

Copy `.env.example` to `.env` and adjust:

```bash
cp .env.example .env
```

Key settings: `PIDOG_MODE`, `LLM_BACKEND`, `OLLAMA_HOST`, `OLLAMA_MODEL`, `BENCH_MODE`.

## Project Structure

```
src/pidog_brain/
  main.py          CLI entry point
  config.py        Environment / .env configuration
  llm/             LLM backends (Ollama, llama.cpp)
  planner/         Prompt builder, schema, parser, policy
  robot/           Robot interface, mock robot, PiDog adapter
  perception/      Sensors, keyboard, voice input
  speech/          STT / TTS
  runtime/         Event loop, logging, telemetry
```
