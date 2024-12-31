from abc import ABC, abstractmethod


class BaseIndexService(ABC):

    @abstractmethod
    async def find_files_to_update(self) -> list[str]:
        raise NotImplementedError

    async def get_info(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def get_clusters(self) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def remove(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, files: list[dict]) -> None:
        raise NotImplementedError
