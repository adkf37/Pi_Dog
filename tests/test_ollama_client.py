import httpx
import pytest

from pidog_brain.config import Settings
from pidog_brain.llm.ollama_client import OllamaClient


def test_ollama_client_uses_config_host_and_model():
    settings = Settings(ollama_host="http://ollama:11434", ollama_model="phi3:mini")
    client = OllamaClient(host=settings.ollama_host, model=settings.ollama_model)
    assert client.host == "http://ollama:11434"
    assert client.model == "phi3:mini"


def test_ollama_client_generates_text(respx_mock):
    respx_mock.post("http://localhost:11434/api/generate").respond(
        json={"response": "Hello world!"}
    )
    client = OllamaClient()
    result = client.generate("Say hello")
    assert result == "Hello world!"


def test_ollama_client_sends_correct_payload(respx_mock):
    respx_mock.post("http://localhost:11434/api/generate").respond(
        json={"response": "ok"}
    )
    client = OllamaClient()
    client.generate("test prompt")
    request = respx_mock.calls.last.request
    import json
    body = json.loads(request.content)
    assert body["model"] == "tinyllama"
    assert body["prompt"] == "test prompt"
    assert body["stream"] is False
    assert body["think"] is False
    assert body["keep_alive"] == -1
    assert body["options"] == {
        "temperature": 0.0,
        "num_predict": 64,
        "num_ctx": 1024,
    }


def test_ollama_client_passes_extra_kwargs(respx_mock):
    respx_mock.post("http://localhost:11434/api/generate").respond(
        json={"response": "ok"}
    )
    client = OllamaClient()
    client.generate("hi", temperature=0.5)
    import json
    body = json.loads(respx_mock.calls.last.request.content)
    assert body["options"]["temperature"] == 0.5


def test_ollama_client_sends_structured_output_format(respx_mock):
    respx_mock.post("http://localhost:11434/api/generate").respond(
        json={"response": "{}"}
    )
    client = OllamaClient()
    schema = {"type": "object"}
    client.generate("hi", format=schema)
    import json
    body = json.loads(respx_mock.calls.last.request.content)
    assert body["format"] == schema


def test_ollama_client_records_metrics(respx_mock):
    respx_mock.post("http://localhost:11434/api/generate").respond(
        json={
            "response": "ok",
            "total_duration": 2_000_000_000,
            "load_duration": 500_000_000,
            "eval_count": 20,
            "eval_duration": 1_000_000_000,
        }
    )
    client = OllamaClient()
    client.generate("hi")
    assert client.last_metrics["total_duration_ms"] == 2000.0
    assert client.last_metrics["load_duration_ms"] == 500.0
    assert client.last_metrics["tokens_per_second"] == 20.0


def test_ollama_client_warmup_loads_without_generating(respx_mock):
    respx_mock.post("http://localhost:11434/api/generate").respond(
        json={"response": "", "load_duration": 250_000_000}
    )
    client = OllamaClient(model="qwen3.5:0.8b")
    metrics = client.warmup()
    import json
    body = json.loads(respx_mock.calls.last.request.content)
    assert body == {
        "model": "qwen3.5:0.8b",
        "prompt": "",
        "stream": False,
        "keep_alive": -1,
    }
    assert metrics["load_duration_ms"] == 250.0


def test_ollama_client_preserves_duration_keep_alive():
    client = OllamaClient(keep_alive="30m")
    assert client.keep_alive == "30m"


def test_ollama_client_converts_numeric_keep_alive_to_integer():
    client = OllamaClient(keep_alive="-1")
    assert client.keep_alive == -1


def test_ollama_client_connection_error():
    client = OllamaClient(host="http://nonexistent:11434")
    with pytest.raises(ConnectionError, match="Could not connect to Ollama"):
        client.generate("hello")


def test_ollama_client_timeout(respx_mock):
    respx_mock.post("http://localhost:11434/api/generate").side_effect = (
        httpx.TimeoutException("timeout")
    )
    client = OllamaClient()
    with pytest.raises(TimeoutError, match="timed out"):
        client.generate("hello")


def test_ollama_client_http_error(respx_mock):
    respx_mock.post("http://localhost:11434/api/generate").respond(status_code=503)
    client = OllamaClient()
    with pytest.raises(RuntimeError, match="Ollama returned HTTP 503"):
        client.generate("hello")


def test_ollama_client_bad_json(respx_mock):
    respx_mock.post("http://localhost:11434/api/generate").respond(
        content="not json"
    )
    client = OllamaClient()
    with pytest.raises(RuntimeError, match="Unexpected Ollama response format"):
        client.generate("hello")
