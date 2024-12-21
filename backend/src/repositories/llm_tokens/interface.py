from typing import Optional
from abc import ABC, abstractmethod


class LLMTokensRepository(ABC):
    @abstractmethod
    async def create(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def add_tokens(self, input_tokens: int, output_tokens: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self) -> Optional[dict]:
        raise NotImplementedError

    @abstractmethod
    async def clean(self) -> None:
        raise NotImplementedError
