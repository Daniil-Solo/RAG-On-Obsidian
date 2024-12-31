from abc import ABC, abstractmethod


class BaseVectorStoreService(ABC):

    @abstractmethod
    async def retrieve(self, query: str, k: int) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def add_chunks(self, texts: list[str], filenames: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_chunks_of_file(self, filename: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_all_chunks(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_chunks_of_file(self, filename: str) -> list[dict]:
        raise NotImplementedError
