from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, delete

from src.database.models import MessageModel
from src.repositories.message.interface import MessageRepository


class MessageSQLAlchemyRepository(MessageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, content: str, role: str) -> dict:
        message = MessageModel(content=content, role=role)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message.model_dump()

    async def get_many(self, limit: int, offset: int) -> list[dict]:
        statement = select(MessageModel).order_by(MessageModel.created_date)
        result = await self.session.execute(statement)
        return [res.model_dump() for res in result.scalars().all()]

    async def clean_all(self) -> None:
        statement = delete(MessageModel)
        await self.session.execute(statement)
        await self.session.commit()
