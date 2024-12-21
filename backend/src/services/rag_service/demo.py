import os
import logging
from uuid import uuid4

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import VectorParams, PointStruct
from qdrant_client.http.models import Distance
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter
from sklearn.decomposition import PCA
import numpy as np

from src.services.rag_service.base import BaseRagService, RagResponse
from src.services.llm_service.base import BaseLLMService


EMBEDDINGS_MODEL_NAME = "intfloat/multilingual-e5-base"
EMBEDDINGS_MODEL_SIZE = 768
SIMILARITY_METRIC = Distance.COSINE
QDRANT_COLLECTION_NAME = "obsidian"

logger = logging.getLogger(__name__)


class CustomTextSplitter:
    def __init__(self, chunk_size=1024, chunk_overlap=512):
        self.chunk_size = chunk_size
        self.splitter_level1 = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator=r'[#]+ ',
            is_separator_regex=True,
            )
        self.splitter_level2 = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator='\n\n',
            is_separator_regex=False,
            )
        self.splitter_level3 = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator='\n',
            is_separator_regex=False,
            )

    def split_text(self, markdown_text: str) -> list[str]:
        chunks = self.splitter_level1.split_text(markdown_text)
        results = []
        for chunk in chunks:
            if len(chunk) > self.chunk_size:
                results.extend(self.splitter_level2.split_text(chunk))
            else:
                results.append(chunk)
        chunks = results
        results = []
        for chunk in chunks:
            if len(chunk) > self.chunk_size:
                results.extend(self.splitter_level3.split_text(chunk))
            else:
                results.append(chunk)
        return results


class DemoQdrantRagService(BaseRagService):

    def __init__(self, qdrant_url: str, llm: BaseLLMService = None):
        self.qdrant_client = AsyncQdrantClient(qdrant_url)
        self.llm = llm

    async def create_vectordb(self, obsidian_path: str):
        if await self.qdrant_client.collection_exists(QDRANT_COLLECTION_NAME):
            logger.info(f"collection {QDRANT_COLLECTION_NAME} already exists")
            return
        await self.qdrant_client.create_collection(
            QDRANT_COLLECTION_NAME,
            VectorParams(
                size=EMBEDDINGS_MODEL_SIZE,
                distance=SIMILARITY_METRIC
            ),
        )
        logger.info(f"Collection {QDRANT_COLLECTION_NAME} has been created successfully")
        sentence_embedder = SentenceTransformer(EMBEDDINGS_MODEL_NAME)
        logger.info(f"Sentence transformer {EMBEDDINGS_MODEL_NAME} has been downloaded successfully")
        text_splitter = CustomTextSplitter()
        for root, _, files in os.walk(obsidian_path):
            for filename in filter(lambda name: name.endswith(".md"), files):
                await self._add_document(root, filename, text_splitter, sentence_embedder)
                logger.info(f"Document {filename} has been processed successfully")

    async def _add_document(self, root: str, filename: str, text_splitter: CustomTextSplitter, sentence_embedder: SentenceTransformer) -> np.ndarray:
        file_path = os.path.join(root, filename)
        embeddings = []

        with open(file_path, 'r') as file:
            content = file.read()

        text_fragments = text_splitter.split_text(content)
        points = []

        for fragment in text_fragments:
            embedding = sentence_embedder.encode(filename[:-3] + " " + fragment)
            embeddings.append(embedding)
            points.append(PointStruct(id=str(uuid4()), vector=embedding, payload={'filename': filename, 'text': fragment}))

        if len(points) == 0:
            return np.zeros((1, EMBEDDINGS_MODEL_SIZE), dtype=np.float32)

        await self.qdrant_client.upsert(collection_name=QDRANT_COLLECTION_NAME, points=points)
        return np.mean(embeddings, axis=0).reshape(1, -1)
        

    async def _remove_document(self, filename: str):
        points_selector = Filter(
            must=[
                FieldCondition(
                    key="filename",
                    match=MatchValue(value=filename),
                )
            ]
        )
        await self.qdrant_client.delete(
            collection_name=QDRANT_COLLECTION_NAME,
            points_selector=points_selector
        )

    async def _retrieve(self, query, k=5):
        sentence_embedder = SentenceTransformer(EMBEDDINGS_MODEL_NAME)
        query_embed = sentence_embedder.encode(query)
        results = await self.qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embed,
            limit=k,
        )
        return results

    async def run(self, user_query: str) -> RagResponse:
        results = await self._retrieve(user_query)
        related_documents = {result.payload['filename'] for result in results}
        logger.info(f"For query '{user_query}' related documents are: {related_documents}")
        retrieved_context = "\n\n".join([result.payload['text'] for result in results])
        prompt = f"""
            Context information is below.
            ---------------------
            {retrieved_context}
            ---------------------
            Given the context information and not prior knowledge, answer the query.
            Query: {user_query}
            Answer:
        """
        answer = await self.llm.run(prompt)
        return RagResponse(answer=answer, related_documents=list(related_documents))

    async def update(self, files_to_update: list[str]) -> list[dict]:
        sentence_embedder = SentenceTransformer(EMBEDDINGS_MODEL_NAME)
        text_splitter = CustomTextSplitter()
        pca = PCA(n_components=2)

        results = []
        embeddings = []

        for file_path in files_to_update:
            filename = os.path.basename(file_path)
            if os.path.exists(file_path):
                await self._remove_document(file_path)
                embedding = await self._add_document(os.path.dirname(file_path), filename, text_splitter, sentence_embedder)
                embeddings.append(embedding)
                results.append({"file_path": file_path})
                logger.info(f"Document {filename} has been updated successfully")
            else:
                await self._remove_document(filename)
                logger.info(f"Document {filename} has been removed successfully")

        if len(embeddings) > 0:  # TODO: does not work correctly if only one file updated
            embeddings = np.stack(embeddings, axis=0).squeeze()
            pca_result = pca.fit_transform(embeddings)
            for i in range(len(results)):
                results[i]["x"] = float(pca_result[i, 0])
                results[i]["y"] = float(pca_result[i, 1])

        return results
