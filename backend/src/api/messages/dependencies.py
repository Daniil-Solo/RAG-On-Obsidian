from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_async_session
from src.repositories.message.interface import MessageRepository
from src.repositories.message.sqlalchemy import MessageSQLAlchemyRepository


def get_message_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> MessageRepository:
    return MessageSQLAlchemyRepository(db_session)
