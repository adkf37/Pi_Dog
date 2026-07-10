from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pidog_mode: str = "mock"
    llm_backend: str = "ollama"
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "tinyllama"
    ollama_timeout_s: float = 5.0
    ollama_warmup_timeout_s: float = 120.0
    ollama_keep_alive: str = "-1"
    ollama_num_predict: int = 64
    ollama_num_ctx: int = 1024
    ollama_temperature: float = 0.0
    ollama_think: bool = False
    ollama_warmup: bool = False
    enable_fast_path: bool = True
    bench_mode: bool = True
    max_actions_per_turn: int = 3
    max_action_duration_s: float = 3.0
    llama_model_path: str = "models/llama-model.gguf"
    enable_voice: bool = False
    enable_camera: bool = False

    @property
    def movement_enabled(self) -> bool:
        return not self.bench_mode

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    return Settings()
