from abc import ABC, abstractmethod


class BaseIndexService(ABC):

    @abstractmethod
    async def find_files_to_update(self) -> list[str]:
        raise NotImplementedError("This method should be implemented")

    async def get_info(self) -> dict:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def get_last_updated_process(self) -> dict:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def get_clusters(self) -> list[dict]:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def remove(self) -> None:
        raise NotImplementedError("This method should be implemented")

    @abstractmethod
    async def update(self, files: list[dict]) -> None:
        raise NotImplementedError("This method should be implemented")
