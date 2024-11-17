from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_async_session
from src.repositories.settings.interface import SettingsRepository
from src.repositories.settings.sqlalchemy import SettingsSQLAlchemyRepository


def get_settings_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> SettingsRepository:
    return SettingsSQLAlchemyRepository(db_session)
