from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pidog_mode: str = "mock"
    llm_backend: str = "ollama"
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "tinyllama"
    bench_mode: bool = True
    max_actions_per_turn: int = 3
    max_action_duration_s: float = 3.0
    enable_voice: bool = False
    enable_camera: bool = False

    @property
    def movement_enabled(self) -> bool:
        return not self.bench_mode

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    return Settings()
