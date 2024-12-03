from abc import ABC, abstractmethod


class MessageRepository(ABC):
    @abstractmethod
    async def create(self, content: str, role: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, limit: int, offset: int) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def clean_all(self) -> None:
        raise NotImplementedError
