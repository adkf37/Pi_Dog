# Data Sources

## Hardware / SDK Documentation

| Source | URL | Availability | Notes |
|--------|-----|-------------|-------|
| SunFounder PiDog Docs | https://docs.sunfounder.com/projects/pidog/en/latest/ | Public online | Primary hardware reference |
| SunFounder PiDog GitHub | https://github.com/sunfounder/pidog | Public repo | Python library source |
| PiDog Ollama Tutorial | https://docs.sunfounder.com/projects/pidog/en/latest/ai_interaction/python_llm_ollama.html | Public online | Reference for Ollama integration pattern |
| PiDog Local Voice Chatbot Tutorial | https://docs.sunfounder.com/projects/pidog/en/latest/ai_interaction/python_local_chatbot.html | Public online | Reference for STT/TTS integration |
| Arm Learning Path — LLM on Pi 5 | https://learn.arm.com/learning-paths/embedded-and-microcontrollers/llama-python-cpu/llama-python-chatbot/ | Public online | Performance reference for Pi 5 LLM inference |

## Model Sources

| Source | Details | Availability | Notes |
|--------|---------|-------------|-------|
| Ollama Library | https://ollama.com/library | Public (needs internet) | Default model source; accessible from Pi via `ollama pull` |
| Hugging Face GGUF models | https://huggingface.co/models?library=gguf | Public | Fallback for llama.cpp path |
| llama-cpp-python | PyPI (`llama-cpp-python`) | Public | Alternative local inference backend |

## Runtime Dependencies (PyPI)

| Package | Purpose | Status |
|---------|---------|--------|
| pydantic | Action schema validation | Available |
| httpx | Ollama API HTTP calls | Available |
| python-dotenv | .env loading | Available |
| pytest | Testing | Available |
| llama-cpp-python | Optional llama.cpp backend | Available |

## Notes

- All data sources are publicly available online. No credentials or API keys required.
- PiDog hardware libraries (`pidog`, `robot-hat`, `vilib`) are installed via SunFounder's setup on the Pi, not pip.
- Model weights are downloaded at runtime by Ollama (`ollama pull`) or placed manually for llama.cpp.
