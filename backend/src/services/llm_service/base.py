from abc import ABC, abstractmethod


class BaseLLMService(ABC):

    @abstractmethod
    async def run(self, query: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def check(self) -> tuple[bool, str]:
        raise NotImplementedError

    @abstractmethod
    async def get_used_tokens(self) -> tuple[int, int]:
        raise NotImplementedError


class LLMError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
