
from pidog_brain.config import Settings


def test_default_settings():
    s = Settings()
    assert s.pidog_mode == "mock"
    assert s.llm_backend == "ollama"
    assert s.ollama_host == "http://localhost:11434"
    assert s.ollama_model == "tinyllama"
    assert s.ollama_timeout_s == 5.0
    assert s.ollama_warmup_timeout_s == 120.0
    assert s.ollama_num_predict == 64
    assert s.ollama_num_ctx == 1024
    assert s.ollama_think is False
    assert s.enable_fast_path is True
    assert s.bench_mode is True
    assert s.max_actions_per_turn == 3
    assert s.max_action_duration_s == 3.0
    assert s.enable_voice is False
    assert s.enable_camera is False


def test_movement_enabled_property():
    assert Settings(bench_mode=True).movement_enabled is False
    assert Settings(bench_mode=False).movement_enabled is True


def test_env_override(monkeypatch):
    monkeypatch.setenv("PIDOG_MODE", "robot")
    monkeypatch.setenv("OLLAMA_MODEL", "phi3:mini")
    monkeypatch.setenv("BENCH_MODE", "false")
    s = Settings()
    assert s.pidog_mode == "robot"
    assert s.ollama_model == "phi3:mini"
    assert s.bench_mode is False
    assert s.movement_enabled is True
