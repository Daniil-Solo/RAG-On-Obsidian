from abc import ABC, abstractmethod


class BaseLLMService(ABC):

    @abstractmethod
    async def run(self, query: str) -> str:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def check(self) -> tuple[bool, str]:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def get_used_tokens(self) -> tuple[int, int]:
        raise NotImplementedError("This method should be implemented")

class LLMException(Exception):
    def __init__(self, message: str):
        self.message = message
