from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.api.general_schemas import MessageResponse
from src.api.index.dependencies import get_index_service
from src.api.messages.dependencies import get_rag_service
from src.api.index.schemas import IndexInfoResponse, ClustersResponse, IndexationProgressResponse
from src.services.rag_service.base import BaseRagService

index_router = APIRouter(prefix="/index", tags=["index"])


@index_router.get("/info/", response_model=IndexInfoResponse)
async def get_index_info(
    index_service: Annotated[BaseRagService, Depends(get_index_service)],
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
    index_service: Annotated[BaseRagService, Depends(get_index_service)],
) -> ClustersResponse:
    clusters = await index_service.get_clusters()
    return ClustersResponse.from_list(clusters)


@index_router.put("/", response_model=MessageResponse)
async def update_index(
    index_service: Annotated[BaseRagService, Depends(get_index_service)],
    rag_service: Annotated[BaseRagService, Depends(get_rag_service)],
) -> MessageResponse:
    files_to_update = await index_service.find_files_to_update()
    files_with_coords = await rag_service.update(files_to_update)
    await index_service.update(files_with_coords)

    return MessageResponse(message="Index updated succesfully")


@index_router.delete("/", response_model=MessageResponse)
async def delete_index(
    index_service: Annotated[BaseRagService, Depends(get_index_service)],
    rag_service: Annotated[BaseRagService, Depends(get_rag_service)],
) -> MessageResponse:
    await index_service.remove()
    await rag_service.remove()
    return MessageResponse(message="Index deleted succesfully")
