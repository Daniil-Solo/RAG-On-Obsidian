import asyncio

from src.services.rag_service.base import BaseRagService, RagResponse


class DummyRagService(BaseRagService):

    async def run(self, user_query: str) -> RagResponse:
        await asyncio.sleep(0.5)
        return RagResponse(answer=user_query, related_documents=["rag.md", "llm.md"], used_tokens=(100, 460))
