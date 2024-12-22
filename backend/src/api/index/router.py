from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from src.api.general_schemas import MessageResponse
from src.api.index.dependencies import get_index_service, get_update_progress_repository
from src.api.index.schemas import ClustersResponse, IndexInfoResponse, IndexProgressResponse
from src.api.messages.dependencies import get_rag_service
from src.repositories.index.interface import UpdateProgressRepository
from src.services.index_service.base import BaseIndexService
from src.services.rag_service.base import BaseRagService

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
    background_tasks: BackgroundTasks,
    index_service: Annotated[BaseIndexService, Depends(get_index_service)],
    rag_service: Annotated[BaseRagService, Depends(get_rag_service)],
    update_progress_repository: Annotated[UpdateProgressRepository, Depends(get_update_progress_repository)],
) -> MessageResponse:
    async def background_indexing() -> None:
        process_id = await update_progress_repository.start_update_process()
        files_to_update = await index_service.find_files_to_update()
        files_with_coords = await rag_service.update(files_to_update)
        await index_service.update(files_with_coords)
        await update_progress_repository.finish_update_process(process_id=process_id)

    background_tasks.add_task(background_indexing)
    return MessageResponse(message="Index update started in the background")


@index_router.put("/progress", response_model=IndexProgressResponse)
async def get_index_progress(
    update_progress_repository: Annotated[UpdateProgressRepository, Depends(get_update_progress_repository)],
) -> IndexProgressResponse:
    stage = await update_progress_repository.get_progress_stage()
    if stage is not None:
        return IndexProgressResponse(name=stage["name"], value=stage["progress"])
    return IndexProgressResponse(name="No active process", value=0)


@index_router.delete("/", response_model=MessageResponse)
async def delete_index(
    index_service: Annotated[BaseRagService, Depends(get_index_service)],
    rag_service: Annotated[BaseRagService, Depends(get_rag_service)],
) -> MessageResponse:
    await index_service.remove()
    await rag_service.remove()
    return MessageResponse(message="Index deleted succesfully")
