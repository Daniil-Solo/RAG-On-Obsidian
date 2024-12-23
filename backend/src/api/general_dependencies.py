from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.llm_tokens.interface import LLMTokensRepository
from src.repositories.llm_tokens.sqlalchemy import LLMTokensSQLAlchemyRepository
from src.database.session import get_async_session
from src.services.rag_service.base import BaseRagService
from src.services.rag_service.final import FinalRagService
from src.services.rag_service.dummy import DummyRagService
from src.services.llm_service.base import BaseLLMService
from src.services.llm_service.builder import LLMServiceBuilder
from src.api.settings.dependencies import get_settings_repository
from src.repositories.settings.interface import SettingsRepository
from src.services.vector_store_service.base import BaseVectorStoreService
from src.services.vector_store_service.pgvector import PGVectorStoreService
from src.services.embeddings_service.base import BaseEmbeddingsService
from src.services.embeddings_service.mistralai import MistralAIEmbeddingsService
from src.config import app_config


def get_llm_tokens_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> LLMTokensRepository:
    return LLMTokensSQLAlchemyRepository(db_session)


async def get_llm_service(
    settings_repository: Annotated[SettingsRepository, Depends(get_settings_repository)],
) -> BaseLLMService:
    settings = await settings_repository.get_llm_settings()
    if not settings:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Requested LLM settings were not found. Set the settings first",
        )
    try:
        llm_service = LLMServiceBuilder.build(**settings)
    except NotImplementedError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Requested LLM type {settings['vendor']} was not found",
        ) from err
    return llm_service


async def get_embeddings_service(
    settings_repository: Annotated[SettingsRepository, Depends(get_settings_repository)],
) -> BaseEmbeddingsService:
    settings = await settings_repository.get_llm_settings()
    if not settings:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Requested LLM settings were not found. Set the settings first",
        )
    return MistralAIEmbeddingsService(api_token=settings["token"])


def get_vector_store_service(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
    embeddings_service: Annotated[BaseEmbeddingsService, Depends(get_embeddings_service)],
) -> BaseVectorStoreService:
    return PGVectorStoreService(db_session, embeddings_service)


def get_rag_service(
    llm_service: Annotated[BaseLLMService, Depends(get_llm_service)],
    vector_store_service: Annotated[BaseVectorStoreService, Depends(get_vector_store_service)],
) -> BaseRagService:
    if app_config.is_debug:
        return DummyRagService()
    return FinalRagService(llm_service, vector_store_service)
