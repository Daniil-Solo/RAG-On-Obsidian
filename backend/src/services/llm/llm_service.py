from abc import ABC, abstractmethod


class LLMService(ABC):

    @abstractmethod
    def check(self) -> bool: ...

    @abstractmethod
    def invoke(self, messages: list[str]) -> str: ...
