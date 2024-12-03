from typing import Literal
from abc import ABC, abstractmethod


class MessageRepository(ABC):
    @abstractmethod
    async def create(self, content: str, role: Literal["user", "assistant"]) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, limit: int, offset: int) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def clean_all(self) -> None:
        raise NotImplementedError
