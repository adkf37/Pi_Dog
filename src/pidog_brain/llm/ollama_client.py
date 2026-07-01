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
        resp = httpx.post(f"{self.host}/api/generate", json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["response"]
