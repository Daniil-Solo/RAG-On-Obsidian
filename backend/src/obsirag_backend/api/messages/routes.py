from typing import Annotated

from fastapi import APIRouter
from fastapi import Query
from pydantic import NonNegativeInt
from pydantic import PositiveInt


from obsirag_backend.api.messages.contracts import MessageResponse
from obsirag_backend.api.messages.contracts import ModelMessageResponse
from obsirag_backend.api.messages.contracts import UserMessageRequest

router = APIRouter(prefix="/api/messages")


@router.get("/")
async def get_chat_messages(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query(le=100)] = 10,
) -> list[MessageResponse]:
    del offset
    return [MessageResponse(role="user", content="", datetime="2024-11-13 23:34:00.000000") for _ in range(limit)]


@router.post("/")
async def post_user_message(user_message: UserMessageRequest) -> ModelMessageResponse:
    return ModelMessageResponse(answer=user_message.content, related_documents=["1.md", "2.md"])
