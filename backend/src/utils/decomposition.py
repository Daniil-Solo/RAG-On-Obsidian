import logging
import os

import numpy as np
from sklearn.decomposition import PCA

from src.repositories.index.interface import FileRepository
from src.services.vector_store_service.base import BaseVectorStoreService

logger = logging.getLogger(__name__)


async def get_decomposition_components(
        file_paths: list[str],
        file_repository: FileRepository,
        vector_store: BaseVectorStoreService
) -> list[dict]:
    if not file_paths:
        return []
    # Retrieve all existing embeddings from the database
    old_file_paths = [file["name"] for file in await file_repository.get_all()]
    current_file_paths = list(set(file_paths) | set(old_file_paths))

    file_paths_to_delete = set()
    embeddings_by_file = []
    for file_path in current_file_paths:
        filename = os.path.basename(file_path)
        chunks = await vector_store.get_chunks_of_file(filename)
        if not chunks:
            logger.info(f"No chunks for{filename}")
            file_paths_to_delete.add(file_path)
            continue
        mean_embedding = np.array([chunk["embedding"] for chunk in chunks]).mean(axis=0)
        logger.info(f"{filename}, shape: {mean_embedding.shape}")
        embeddings_by_file.append(mean_embedding)

    mean_embeddings = np.array(embeddings_by_file)
    decomposition_result = PCA(n_components=2).fit_transform(mean_embeddings)

    for file_path in file_paths_to_delete:
        current_file_paths.remove(file_path)

    results = [
        {
            "file_path": file_path,
            "x": float(decomposition_result[index, 0]),
            "y": float(decomposition_result[index, 1]),
            "is_removed": False
        }
        for index, file_path in enumerate(current_file_paths)
    ]
    results.extend(
        [
            {"file_path": file_path, "x": 0, "y": 0, "is_removed": True}
            for file_path in file_paths_to_delete
        ]
    )

    logger.info("PCA over embeddings calculated successfully")
    return results
