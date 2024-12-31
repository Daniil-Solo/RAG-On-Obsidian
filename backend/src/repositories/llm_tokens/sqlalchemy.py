from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update

from src.database.models import LLMTokensModel
from src.repositories.llm_tokens.interface import LLMTokensRepository


class LLMTokensSQLAlchemyRepository(LLMTokensRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self) -> dict:
        llm_tokens = LLMTokensModel(input_tokens=0, output_tokens=0)
        self.session.add(llm_tokens)
        await self.session.commit()
        await self.session.refresh(llm_tokens)
        return llm_tokens.model_dump()

    async def add_tokens(self, input_tokens: int, output_tokens: int) -> None:
        existing_llm_tokens = await self.get()
        if not existing_llm_tokens:
            llm_tokens = LLMTokensModel(input_tokens=input_tokens, output_tokens=output_tokens)
            self.session.add(llm_tokens)
        else:
            statement = (
                update(LLMTokensModel)
                .values(
                    input_tokens=LLMTokensModel.input_tokens + input_tokens,
                    output_tokens=LLMTokensModel.output_tokens + output_tokens,
                )
            )
            await self.session.execute(statement)
        await self.session.commit()

    async def get(self) -> Optional[dict]:
        statement = select(LLMTokensModel)
        result = await self.session.execute(statement)
        llm_tokens = result.scalars().first()
        return llm_tokens and llm_tokens.model_dump()

    async def clean(self) -> None:
        statement = (
            update(LLMTokensModel)
            .values(
                input_tokens=0,
                output_tokens=0,
            )
        )
        await self.session.execute(statement)
        await self.session.commit()
