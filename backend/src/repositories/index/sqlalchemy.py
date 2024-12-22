from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, delete, update

from src.database.models import FileModel, IndexInfoModel
from src.repositories.index.interface import FileRepository


class FileSQLAlchemyRepository(FileRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, name: str, size: int, updated_at: datetime, x: float, y: float) -> None:
        file_record = FileModel(name=name, size=size, updated_at=updated_at, x=x, y=y)
        self.session.add(file_record)
        await self.session.commit()

    async def update(self, name: str, size: int, updated_at: datetime, x: float, y: float) -> None:
        statement = select(FileModel).where(FileModel.name == name)
        results = await self.session.execute(statement)
        file_record = results.first()

        await self._update_index_info(datetime.utcnow())
        if file_record is None:
            await self.add(
                name=name,
                size=size,
                updated_at=updated_at,
                x=x,
                y=y,
            )
        else:
            statement = (
                update(FileModel)
                .values(
                    name=name,
                    size=size,
                    updated_at=updated_at,
                    x=x,
                    y=y,
                )
            )
            await self.session.execute(statement)
            await self.session.commit()

    async def get_index_info(self) -> dict | None:
        statement = select(IndexInfoModel)
        result = await self.session.execute(statement)
        info = result.scalars().first()
        return info and info.model_dump()

    async def delete(self, name: str) -> None:
        statement = select(FileModel).where(FileModel.name == name)
        results = await self.session.execute(statement)
        file_record = results.one()

        await self.session.delete(file_record)
        await self.session.commit()

    async def get_all(self) -> list[dict]:
        statement = select(FileModel)
        results = await self.session.execute(statement)
        files = results.scalars().all()
        return [file.model_dump() for file in files]

    async def _update_index_info(self, last_update_time: datetime) -> None:
        info = await self.get_index_info()
        if info is None:
            info = IndexInfoModel(last_update_time=last_update_time)
            self.session.add(info)
        else:
            statement = update(IndexInfoModel).values(last_update_time=last_update_time)
            await self.session.execute(statement)

        await self.session.commit()
