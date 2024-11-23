from src.services.llm.llm_service import LLMService


class DummyLLMService(LLMService):
    def __init__(self) -> None:
        super().__init__()

    def check(self) -> bool:
        return True

    def invoke(self, messages: list[str]) -> str:
        del messages
        return "output"
