from pidog_brain.llm.base import LLMBase


class LlamaCppClient(LLMBase):
    def __init__(self, model_path: str, **kwargs):
        self.model_path = model_path
        self._llm = None

    def _ensure_model(self):
        if self._llm is None:
            from llama_cpp import Llama

            self._llm = Llama(model_path=self.model_path)

    def generate(self, prompt: str, **kwargs) -> str:
        self._ensure_model()
        output = self._llm(prompt, **kwargs)
        return output["choices"][0]["text"]
