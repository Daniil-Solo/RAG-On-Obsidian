from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import app_config
from src.database.session import get_async_session
from src.repositories.index.interface import FileRepository, UpdateProgressRepository
from src.repositories.index.sqlalchemy import FileSQLAlchemyRepository, UpdateProgressSQLAlchemyRepository
from src.services.index_service.base import BaseIndexService
from src.services.index_service.final import DemoIndexService


def get_file_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> FileRepository:
    return FileSQLAlchemyRepository(db_session)


def get_update_progress_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UpdateProgressRepository:
    return UpdateProgressSQLAlchemyRepository(db_session)


def get_index_service(
    file_repository: Annotated[FileRepository, Depends(get_file_repository)],
    update_progress_repository: Annotated[UpdateProgressRepository, Depends(get_update_progress_repository)],
) -> BaseIndexService:
    return DemoIndexService(
        obsidian_path=app_config.OBSIDIAN_PATH,
        file_repository=file_repository,
        update_progress_repository=update_progress_repository,
    )
