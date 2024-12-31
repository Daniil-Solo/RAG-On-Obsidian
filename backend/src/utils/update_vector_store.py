import logging
import os

import aiofiles

from src.repositories.index.interface import UpdateProgressRepository
from src.services.vector_store_service.base import BaseVectorStoreService
from src.utils.text_splitter import CustomTextSplitter

logger = logging.getLogger(__name__)


async def update_vector_store(
        files_to_update: list[str],
        update_progress_repository: UpdateProgressRepository,
        vector_store: BaseVectorStoreService
) -> None:
    text_splitter = CustomTextSplitter()

    process = await update_progress_repository.get_update_process()
    stage_id = await update_progress_repository.start_progress_stage(name="1. Vectorization", process_id=process["id"])
    for idx, file_path in enumerate(files_to_update):
        await update_progress_repository.update_progress_stage(
            stage_id=stage_id,
            progress=int(idx / len(files_to_update) * 100),
        )
        filename = os.path.basename(file_path)
        if os.path.exists(file_path):
            # Remove old data and add updated data
            await vector_store.remove_chunks_of_file(filename)
            async with aiofiles.open(file_path, encoding="utf-8") as f:
                content = await f.read()
            text_chunks = text_splitter.split(filename[:-3] + " " + content)
            await vector_store.add_chunks(text_chunks, [filename] * len(text_chunks))
            logger.info(f"Document {filename} has been updated successfully")
        else:
            # Remove document if it no longer exists
            await vector_store.remove_chunks_of_file(filename)
            logger.info(f"Document {filename} has been removed successfully")

    await update_progress_repository.finish_progress_stage(stage_id=stage_id)
