from abc import ABC, abstractmethod
from datetime import datetime
from typing import Literal


class FileRepository(ABC):
    @abstractmethod
    async def add(self, name: str, size: int, updated_at: datetime, x: float, y: float) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, name: str, size: int, updated_at: datetime, x: float, y: float) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[dict]:
        raise NotImplementedError


class UpdateProgressRepository(ABC):
    @abstractmethod
    async def start_update_process(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_update_process(self) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    async def finish_update_process(self, process_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start_progress_stage(self, name: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_progress_stage(self) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    async def update_progress_stage(self, stage_id: int, progress: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def finish_progress_stage(self, stage_id: int) -> None:
        raise NotImplementedError
