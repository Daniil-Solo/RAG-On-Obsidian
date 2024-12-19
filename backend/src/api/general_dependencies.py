from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_async_session
from src.repositories.llm_tokens.interface import LLMTokensRepository
from src.repositories.llm_tokens.sqlalchemy import LLMTokensSQLAlchemyRepository


def get_llm_tokens_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> LLMTokensRepository:
    return LLMTokensSQLAlchemyRepository(db_session)
