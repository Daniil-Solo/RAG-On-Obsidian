from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_async_session
from src.repositories.message.interface import MessageRepository
from src.repositories.message.sqlalchemy import MessageSQLAlchemyRepository
from src.services.rag_service.base import BaseRagService
from src.services.rag_service.demo import DemoQdrantRagService
from src.services.llm_service.base import BaseLLMService
from src.services.llm_service.builder import LLMServiceBuilder
from src.api.settings.dependencies import get_settings_repository
from src.repositories.settings.interface import SettingsRepository
from src.config import app_config
from fastapi import HTTPException
from http import HTTPStatus


def get_message_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> MessageRepository:
    return MessageSQLAlchemyRepository(db_session)


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


def get_rag_service(
        llm_service: Annotated[BaseLLMService, Depends(get_llm_service)],
) -> BaseRagService:
    return DemoQdrantRagService(qdrant_url=app_config.QDRANT_URL, llm=llm_service)
