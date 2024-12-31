from abc import ABC, abstractmethod


class BaseEmbeddingsService(ABC):

    @abstractmethod
    async def embed_one(self, query: str) -> list[float]:
        raise NotImplementedError

    @abstractmethod
    async def embed_many(self, queries: list[str]) -> list[list[float]]:
        raise NotImplementedError

    @abstractmethod
    async def get_used_tokens(self) -> tuple[int, int]:
        raise NotImplementedError


class EmbeddingsError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
