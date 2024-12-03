from abc import ABC, abstractmethod


class BaseChecker(ABC):

    @abstractmethod
    async def check(self) -> tuple[bool, str]:
        raise NotImplementedError("This method should be implemented")
