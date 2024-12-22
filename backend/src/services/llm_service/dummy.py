from src.services.llm_service.base import BaseLLMService


class DummyLLMService(BaseLLMService):

    async def run(self, query: str) -> str:
        raise query

    async def check(self) -> tuple[bool, str]:
        return True, ""

    async def get_used_tokens(self) -> tuple[int, int]:
        return 100, 1200
