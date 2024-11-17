from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.api.settings.dependencies import get_settings_repository
from src.api.settings.schemas import LLMSettingsRequest, LLMSettingsResponse
from src.repositories.settings.interface import SettingsRepository

settings_router = APIRouter(prefix="/settings")


@settings_router.get("/llm", response_model=LLMSettingsResponse)
async def get_llm_settings(
    settings_repo: Annotated[SettingsRepository, Depends(get_settings_repository)],
) -> LLMSettingsResponse:
    llm_settings_dict = await settings_repo.get_llm_settings()
    llm_settings_dict = llm_settings_dict or {}
    return LLMSettingsResponse(**llm_settings_dict)


@settings_router.put("/llm")
async def post_user_message(
    llm_settings: LLMSettingsRequest,
    settings_repo: Annotated[SettingsRepository, Depends(get_settings_repository)],
) -> JSONResponse:
    await settings_repo.update_llm_settings(
        model_type=llm_settings.model_type,
        token=llm_settings.token,
        model_name=llm_settings.model_name,
        max_length=llm_settings.max_length,
    )
    return JSONResponse(content={"message": "LLM Settings updated successfully"})
