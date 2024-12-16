import asyncio
from src.services.rag.base import BaseRag, RagResponse


class DummyRag(BaseRag):

    async def run(self, user_query: str) -> RagResponse:
        await asyncio.sleep(0.5)
        return RagResponse(answer=user_query, related_documents=["rag.md", "llm.md"])
