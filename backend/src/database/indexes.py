from sqlalchemy import Index

from src.database.models import ChunkEmbeddingModel

embedding_index = Index(
    "chunk_embed_idx",
    ChunkEmbeddingModel.embedding,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding": "vector_cosine_ops"}
)
