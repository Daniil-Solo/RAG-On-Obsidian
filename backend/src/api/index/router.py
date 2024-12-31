from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.general_dependencies import get_vector_store_service
from src.api.general_schemas import MessageResponse
from src.api.index.dependencies import get_file_repository, get_index_service, get_update_progress_repository
from src.api.index.schemas import ClustersResponse, IndexInfoResponse, StageProgressSchema, UpdateIndexProgressResponse
from src.repositories.index.interface import FileRepository, UpdateProgressRepository
from src.services.index_service.base import BaseIndexService
from src.services.vector_store_service.base import BaseVectorStoreService
from src.utils.decomposition import get_decomposition_components
from src.utils.update_vector_store import update_vector_store

index_router = APIRouter(prefix="/index", tags=["index"])


@index_router.get("/info/", response_model=IndexInfoResponse)
async def get_index_info(
    index_service: Annotated[BaseIndexService, Depends(get_index_service)],
) -> IndexInfoResponse:
    info = await index_service.get_info()

    return IndexInfoResponse(
        n_documents_to_update=info["n_documents_to_update"],
        n_all_documents=info["n_all_documents"],
        last_update_time=info["last_update_time"],
        in_update_process=info["in_update_process"],
    )


@index_router.get("/clusters", response_model=ClustersResponse)
async def get_clusters(
    index_service: Annotated[BaseIndexService, Depends(get_index_service)],
) -> ClustersResponse:
    clusters = await index_service.get_clusters()
    return ClustersResponse.from_list(clusters)


@index_router.put("/", response_model=MessageResponse)
async def update_index(
    index_service: Annotated[BaseIndexService, Depends(get_index_service)],
    vector_store_service: Annotated[BaseVectorStoreService, Depends(get_vector_store_service)],
    update_progress_repository: Annotated[UpdateProgressRepository, Depends(get_update_progress_repository)],
    file_repository: Annotated[FileRepository, Depends(get_file_repository)],
) -> MessageResponse:
    current_process = await update_progress_repository.get_update_process()
    if current_process:
        return MessageResponse(message="The index update operation has already started")

    process_id = await update_progress_repository.start_update_process()
    files_to_update = await index_service.find_files_to_update()
    await update_vector_store(files_to_update, update_progress_repository, vector_store_service)
    results = await get_decomposition_components(files_to_update, file_repository, vector_store_service)
    await index_service.update(results)
    await update_progress_repository.finish_update_process(process_id=process_id)

    return MessageResponse(message="Index has been updated")


@index_router.get("/progress", response_model=UpdateIndexProgressResponse)
async def get_index_progress(
    update_progress_repository: Annotated[UpdateProgressRepository, Depends(get_update_progress_repository)],
) -> UpdateIndexProgressResponse:
    process = await update_progress_repository.get_update_process()
    if not process:
        return UpdateIndexProgressResponse(in_progress=False, stages=[])
    stages = await update_progress_repository.get_stages_by_process(process["id"])
    return UpdateIndexProgressResponse(
        in_progress=True,
        stages=[
            StageProgressSchema(name=stage["name"], value=stage["progress"])
            for stage in stages
        ]
    )


@index_router.delete("/", response_model=MessageResponse)
async def delete_index(
    index_service: Annotated[BaseIndexService, Depends(get_index_service)],
    vector_store_service: Annotated[BaseVectorStoreService, Depends(get_vector_store_service)],
) -> MessageResponse:
    await vector_store_service.remove_all_chunks()
    await index_service.remove()
    return MessageResponse(message="Index deleted successfully")
