from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class RagResponse:
    answer: str
    related_documents: list[str]


class BaseRagService(ABC):

    @abstractmethod
    async def run(self, user_query: str) -> RagResponse:
        raise NotImplementedError
