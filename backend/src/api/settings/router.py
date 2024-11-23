from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.api.settings.dependencies import get_settings_repository
from src.api.settings.schemas import LLMSettingsRequest, LLMSettingsResponse
from src.repositories.settings.interface import SettingsRepository
from src.services.llm import LLMServiceBuilder

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


@settings_router.post(
    "/llm/checking",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully check LLM availability",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to found requested LLM type",
        },
    },
)
async def check_llm_availability(
    llm_settings: LLMSettingsRequest,
) -> JSONResponse:
    try:
        llm_service = LLMServiceBuilder.create(**llm_settings.model_dump())
    except NotImplementedError as err:
        raise HTTPException from err(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Requested model type {llm_settings.model_type} was not found",
        )
    is_available = llm_service.check()
    return JSONResponse(content={"is_available": is_available})
