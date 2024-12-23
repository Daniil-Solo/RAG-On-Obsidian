import asyncio

from sqlmodel import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.vector_store_service.base import BaseVectorStoreService
from src.services.embeddings_service.base import BaseEmbeddingsService, EmbeddingsException
from src.database.models import ChunkEmbeddingModel


class PGVectorStoreService(BaseVectorStoreService):
    def __init__(self, session: AsyncSession, embedding_service: BaseEmbeddingsService):
        self.session = session
        self.embedding_service = embedding_service

    async def retrieve(self, query: str, k: int) -> list[dict]:
        embed = await self.embedding_service.embed_one(query)
        statement = (
            select(ChunkEmbeddingModel)
            .order_by(ChunkEmbeddingModel.embedding.cosine_distance(embed))
            .limit(k)
        )
        results = await self.session.execute(statement)
        chunks = results.scalars().all()
        return [chunk.model_dump() for chunk in chunks]

    async def add_chunks(self, texts: list[str], filenames: list[str]) -> None:
        try:
            embeds = await self.embedding_service.embed_many(texts)
        except EmbeddingsException:
            await asyncio.sleep(2)
            embeds = await self.embedding_service.embed_many(texts)
        for embed, text, filename in zip(embeds, texts, filenames):
            chunk_embedding = ChunkEmbeddingModel(filename=filename, text=text, embedding=embed)
            self.session.add(chunk_embedding)
        await self.session.commit()

    async def remove_chunks_of_file(self, filename: str) -> None:
        statement = (
            delete(ChunkEmbeddingModel)
            .where(ChunkEmbeddingModel.filename == filename)
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def remove_all_chunks(self) -> None:
        statement = delete(ChunkEmbeddingModel)
        await self.session.execute(statement)
        await self.session.commit()

    async def get_chunks_of_file(self, filename: str) -> list[dict]:
        statement = (
            select(ChunkEmbeddingModel)
            .where(ChunkEmbeddingModel.filename == filename)
        )
        results = await self.session.execute(statement)
        files = results.scalars().all()
        return [file.model_dump() for file in files]