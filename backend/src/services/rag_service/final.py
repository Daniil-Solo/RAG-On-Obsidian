import logging
import asyncio
from src.services.llm_service.base import BaseLLMService, LLMException
from src.services.vector_store_service.base import BaseVectorStoreService
from src.services.rag_service.base import BaseRagService, RagResponse


logger = logging.getLogger(__name__)

PROMPT = """\
Context information is below.
---------------------
%s
---------------------
Given the context information and not prior knowledge, answer the query.
Query: %s
Answer:
"""


class FinalRagService(BaseRagService):
    def __init__(self, llm: BaseLLMService = None, vector_store: BaseVectorStoreService = None):
        self.llm = llm
        self.vector_store = vector_store

    async def run(self, user_query: str) -> RagResponse:
        fragments = await self.vector_store.retrieve(user_query, k=5)
        related_documents = {fragment['filename'] for fragment in fragments}
        logger.info(f"Retrieved fragments: {fragments}")
        retrieved_context = "\n\n".join([fragment['text'] for fragment in fragments])
        prompt = PROMPT % (retrieved_context, user_query)
        try:
            answer = await self.llm.run(prompt)
        except LLMException as ex:
            logger.warning(f"Error: {str(ex)}")
            await asyncio.sleep(2)
            answer = await self.llm.run(prompt)
        used_tokens = await self.llm.get_used_tokens()
        return RagResponse(answer=answer, related_documents=list(related_documents), used_tokens=used_tokens)
