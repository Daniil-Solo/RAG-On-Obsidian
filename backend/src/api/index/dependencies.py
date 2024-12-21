from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_async_session
from src.repositories.index.interface import FileRepository
from src.repositories.index.sqlalchemy import FileSQLAlchemyRepository
from src.services.index_service.base import BaseIndexService
from src.services.index_service.demo import DemoIndexService
from src.config import app_config
from fastapi import HTTPException
from http import HTTPStatus


def get_file_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> FileRepository:
    return FileSQLAlchemyRepository(db_session)


def get_index_service(
    file_repository: Annotated[FileRepository, Depends(get_file_repository)],
) -> BaseIndexService:
    return DemoIndexService(obsidian_path=app_config.OBSIDIAN_PATH, file_repository=file_repository)
