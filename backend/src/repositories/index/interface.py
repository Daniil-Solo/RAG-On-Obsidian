from datetime import datetime
from typing import Literal
from abc import ABC, abstractmethod


class FileRepository(ABC):
    @abstractmethod
    async def add(self, name: str, size: int, updated_at: datetime, x: float, y: float) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def update(self, name: str, size: int, updated_at: datetime, x: float, y: float) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[dict]:
        raise NotImplementedError    
