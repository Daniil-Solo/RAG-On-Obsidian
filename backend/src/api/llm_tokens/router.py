from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.general_dependencies import get_llm_tokens_repository
from src.api.llm_tokens.schemas import LLMTokensResponse
from src.repositories.llm_tokens.interface import LLMTokensRepository

llm_tokens_router = APIRouter(prefix="/llm_tokens", tags=["llm tokens"])


@llm_tokens_router.get("/", response_model=LLMTokensResponse)
async def get_llm_tokens(
    llm_tokens_repo: Annotated[LLMTokensRepository, Depends(get_llm_tokens_repository)],
) -> LLMTokensResponse:
    llm_tokens_dict = await llm_tokens_repo.get()
    if not llm_tokens_dict:
        llm_tokens_dict = await llm_tokens_repo.create()
    return LLMTokensResponse(**llm_tokens_dict)
