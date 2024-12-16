from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import NonNegativeInt, PositiveInt

from src.api.messages.dependencies import get_message_repository, get_rag_service
from src.api.messages.schemas import AnswerResponse, MessageHistoryResponse, MessageSchema, QueryRequest
from src.api.general_schemas import MessageResponse
from src.repositories.message.interface import MessageRepository
from src.services.rag.base import BaseRag

messages_router = APIRouter(prefix="/messages", tags=["messages"])


@messages_router.get("/", response_model=MessageHistoryResponse)
async def get_chat_messages(
    message_repo: Annotated[MessageRepository, Depends(get_message_repository)],
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query(le=100)] = 10,
) -> MessageHistoryResponse:
    message_dicts = await message_repo.get_many(limit, offset)
    return MessageHistoryResponse(messages=[MessageSchema(**message_dict) for message_dict in message_dicts])


@messages_router.post("/", response_model=AnswerResponse)
async def post_user_message(
    user_message: QueryRequest,
    message_repo: Annotated[MessageRepository, Depends(get_message_repository)],
    rag_service: Annotated[BaseRag, Depends(get_rag_service)],
) -> AnswerResponse:
    await message_repo.create(content=user_message.content, role="user")
    result = await rag_service.run(user_message.content)
    await message_repo.create(content=result.answer, role="assistant")
    return AnswerResponse(
        answer=result.answer,
        related_documents=result.related_documents,
    )


@messages_router.delete("/", response_model=MessageResponse)
async def clean_message_history(
    message_repo: Annotated[MessageRepository, Depends(get_message_repository)],
) -> MessageResponse:
    await message_repo.clean_all()
    return MessageResponse(
        message="All messages have been successfully deleted"
    )