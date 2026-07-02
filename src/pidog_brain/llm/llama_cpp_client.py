from pidog_brain.llm.base import LLMBase


class LlamaCppClient(LLMBase):
    def __init__(self, model_path: str, **kwargs):
        self.model_path = model_path

    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError(
            "LlamaCppClient is a stub. Install llama-cpp-python and enable "
            "the 'llama' extra to use this backend."
        )
