from gigachat.exceptions import ResponseError
from langchain_community.chat_models import GigaChat
from langchain_core.messages import SystemMessage
from langchain_core.runnables import ConfigurableField

from src.services.llm.llm_service import LLMService


class GigaChatLLMService(LLMService):
    def __init__(self, model_name: str, token: str, max_length: int | None = None) -> None:
        super().__init__()
        self._model_name = model_name
        self._model = GigaChat(
            model=self._model_name,
            credentials=token,
            verify_ssl_certs=False,
            max_tokens=max_length,
        ).configurable_fields(
            max_tokens=ConfigurableField(id="max_tokens"),
        )

    def check(self) -> bool:
        try:
            # generate 6 tokens to pass the check
            self._model.with_config(configurable={"max_tokens": 1}).generate([[SystemMessage(".")]])
        except ResponseError:
            return False
        else:
            return True

    def invoke(self, messages: list[str]) -> str:
        response = self._model.invoke(messages)
        return response.content
