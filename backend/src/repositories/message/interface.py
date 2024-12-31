from abc import ABC, abstractmethod
from typing import Literal


class MessageRepository(ABC):
    @abstractmethod
    async def create(self, content: str, role: Literal["user", "assistant"]) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def clean_all(self) -> None:
        raise NotImplementedError
