from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RagResponse:
    answer: str
    related_documents: list[str]
    used_tokens: tuple[int, int]


class BaseRagService(ABC):

    @abstractmethod
    async def run(self, user_query: str) -> RagResponse:
        raise NotImplementedError
