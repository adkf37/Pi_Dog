# Task 06 — Ollama Client

**Phase:** 1 — LLM Integration
**Profile:** build
**Dependencies:** task-02
**Status:** pending

## Description

Implement `src/pidog_brain/llm/` with `base.py` (abstract LLM interface), `ollama_client.py` (calls local Ollama API), and `llama_cpp_client.py` (stub for future). Keep LLM clients independent of PiDog hardware.

## Inputs

- Task 02 output (config with `LLM_BACKEND`, `OLLAMA_HOST`, `OLLAMA_MODEL`)

## Outputs

- `src/pidog_brain/llm/__init__.py`
- `src/pidog_brain/llm/base.py` — abstract `LLMBase` class
- `src/pidog_brain/llm/ollama_client.py` — Ollama API via httpx
- `src/pidog_brain/llm/llama_cpp_client.py` — stub (raises NotImplementedError)

## Acceptance Checks

- [ ] `OllamaClient.generate(prompt)` returns response text
- [ ] Client reads host/model from config
- [ ] Timeout / connection error is handled gracefully
- [ ] Unit tests with mocked HTTP responses
