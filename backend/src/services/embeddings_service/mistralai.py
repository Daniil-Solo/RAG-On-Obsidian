import json
import aiohttp
import asyncio
import logging
from src.services.embeddings_service.base import BaseEmbeddingsService, EmbeddingsException

EMBED_LINK = "https://api.mistral.ai/v1/embeddings"
EMBED_MODEL = "mistral-embed"
EMBED_ENCODING_FORMAT = "float"
EMBED_SLEEP_TIME = 2  # seconds

logger = logging.getLogger(__name__)


class MistralAIEmbeddingsService(BaseEmbeddingsService):
    def __init__(self, api_token: str, batch_size=10, progress_callback=None) -> None:
        self.api_token = api_token
        self.batch_size = batch_size
        self.progress_callback = progress_callback
        self.input_tokens = 0
        self.output_tokens = 0

    async def _run(self, queries: list[str]) -> list[list[float]]:
        async with aiohttp.ClientSession() as client:
            payload = {
                "model": EMBED_MODEL,
                "encoding_format": EMBED_ENCODING_FORMAT,
                "input": queries,
            }
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                "Authorization": f"Bearer {self.api_token}"
            }
            async with client.post(EMBED_LINK, json=payload, headers=headers) as resp:
                logger.info(f"Embedding response status code: {resp.status}")
                result = await resp.content.read()
                logger.info(f"Embedding response content: {result}")
                if resp.status != 200:
                    raise EmbeddingsException(result.decode("utf-8"))
        result_dict = json.loads(result)
        self.input_tokens += result_dict["usage"]["prompt_tokens"]
        self.output_tokens += result_dict["usage"]["completion_tokens"]
        return [item["embedding"] for item in result_dict["data"]]

    async def embed_one(self, query: str) -> list[float]:
        embeds = await self._run([query])
        return embeds[0]

    async def embed_many(self, queries: list[str]) -> list[list[float]]:
        embeds = []
        for i in range(0, len(queries), self.batch_size):
            batch_queries = queries[i:i+self.batch_size]
            batch_embeds = await self._run(batch_queries)
            embeds.extend(batch_embeds)
            await asyncio.sleep(EMBED_SLEEP_TIME)
            if self.progress_callback:
                self.progress_callback((i + self.batch_size) / len(queries) * 100)
        return embeds

    async def get_used_tokens(self) -> tuple[int, int]:
        return self.input_tokens, self.output_tokens
