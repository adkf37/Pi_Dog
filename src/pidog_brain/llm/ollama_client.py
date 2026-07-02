import json

import httpx

from pidog_brain.llm.base import LLMBase


class OllamaClient(LLMBase):
    def __init__(self, host: str = "http://localhost:11434", model: str = "tinyllama"):
        self.host = host.rstrip("/")
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            **kwargs,
        }
        try:
            resp = httpx.post(f"{self.host}/api/generate", json=payload, timeout=60)
            resp.raise_for_status()
            return resp.json()["response"]
        except httpx.ConnectError:
            raise ConnectionError(
                f"Could not connect to Ollama at {self.host}. "
                f"Is Ollama running?"
            )
        except httpx.TimeoutException:
            raise TimeoutError(
                f"Ollama at {self.host} timed out after 60s for model {self.model}."
            )
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Ollama returned HTTP {e.response.status_code}: {e.response.text}"
            )
        except (json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Unexpected Ollama response format: {e}")
