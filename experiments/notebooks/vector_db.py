from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams

from embedder import VECTOR_SIZE
from config import vector_similarty_metric


url = "http://localhost:6333"
collection_name = "obsidian-vault"

qdrant_client = QdrantClient(url)

if not qdrant_client.collection_exists(collection_name):
    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=VECTOR_SIZE[0],
            distance=vector_similarty_metric),
    )
