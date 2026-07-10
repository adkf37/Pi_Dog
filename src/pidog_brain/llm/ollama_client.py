import json
from typing import Any

import httpx

from pidog_brain.llm.base import LLMBase


class OllamaClient(LLMBase):
    _OPTION_KEYS = {
        "temperature",
        "num_predict",
        "num_ctx",
        "seed",
        "top_k",
        "top_p",
    }

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "tinyllama",
        *,
        timeout_s: float = 5.0,
        warmup_timeout_s: float = 120.0,
        keep_alive: str | int = "-1",
        num_predict: int = 64,
        num_ctx: int = 1024,
        temperature: float = 0.0,
        think: bool = False,
    ):
        self.host = host.rstrip("/")
        self.model = model
        self.timeout_s = timeout_s
        self.warmup_timeout_s = warmup_timeout_s
        self.keep_alive = keep_alive
        self.think = think
        self.default_options = {
            "temperature": temperature,
            "num_predict": num_predict,
            "num_ctx": num_ctx,
        }
        timeout = httpx.Timeout(timeout_s, connect=min(timeout_s, 1.0))
        self._client = httpx.Client(timeout=timeout)
        self.last_metrics: dict[str, float | int | str] = {}

    def generate(self, prompt: str, **kwargs) -> str:
        options = dict(self.default_options)
        options.update(kwargs.pop("options", {}))
        for key in self._OPTION_KEYS:
            if key in kwargs:
                options[key] = kwargs.pop(key)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "think": self.think,
            "keep_alive": self.keep_alive,
            "options": options,
            **kwargs,
        }
        self.last_metrics = {}
        try:
            resp = self._client.post(f"{self.host}/api/generate", json=payload)
            resp.raise_for_status()
            data = resp.json()
            self.last_metrics = self._extract_metrics(data)
            return data["response"]
        except httpx.ConnectError:
            raise ConnectionError(
                f"Could not connect to Ollama at {self.host}. "
                f"Is Ollama running?"
            )
        except httpx.TimeoutException:
            raise TimeoutError(
                f"Ollama at {self.host} timed out after {self.timeout_s:g}s "
                f"for model {self.model}."
            )
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Ollama returned HTTP {e.response.status_code}: {e.response.text}"
            )
        except (json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Unexpected Ollama response format: {e}")

    def warmup(self) -> dict[str, float | int | str]:
        payload = {
            "model": self.model,
            "prompt": "",
            "stream": False,
            "keep_alive": self.keep_alive,
        }
        try:
            timeout = httpx.Timeout(
                self.warmup_timeout_s,
                connect=min(self.warmup_timeout_s, 1.0),
            )
            resp = self._client.post(
                f"{self.host}/api/generate",
                json=payload,
                timeout=timeout,
            )
            resp.raise_for_status()
            self.last_metrics = self._extract_metrics(resp.json())
            return dict(self.last_metrics)
        except httpx.ConnectError:
            raise ConnectionError(
                f"Could not connect to Ollama at {self.host}. Is Ollama running?"
            )
        except httpx.TimeoutException:
            raise TimeoutError(
                f"Ollama warmup timed out after {self.warmup_timeout_s:g}s "
                f"for model {self.model}."
            )
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Ollama returned HTTP {e.response.status_code}: {e.response.text}"
            )
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Unexpected Ollama response format: {e}")

    def close(self) -> None:
        self._client.close()

    @staticmethod
    def _extract_metrics(data: dict[str, Any]) -> dict[str, float | int | str]:
        metrics: dict[str, float | int | str] = {}
        for key in ("total_duration", "load_duration", "prompt_eval_duration", "eval_duration"):
            value = data.get(key)
            if isinstance(value, (int, float)):
                metrics[f"{key}_ms"] = round(value / 1_000_000, 3)

        for key in ("prompt_eval_count", "eval_count", "done_reason"):
            value = data.get(key)
            if isinstance(value, (int, str)):
                metrics[key] = value

        eval_count = data.get("eval_count")
        eval_duration = data.get("eval_duration")
        if (
            isinstance(eval_count, int)
            and isinstance(eval_duration, (int, float))
            and eval_duration
        ):
            tokens_per_second = eval_count / (eval_duration / 1_000_000_000)
            metrics["tokens_per_second"] = round(tokens_per_second, 2)
        return metrics
