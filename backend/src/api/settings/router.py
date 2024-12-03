from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.api.general_schemas import MessageResponse
from src.api.settings.dependencies import get_settings_repository
from src.api.settings.schemas import LLMAvailabilityResponse, LLMSettingsRequest, LLMSettingsResponse
from src.repositories.settings.interface import SettingsRepository
from src.services.llm_checker.builder import LLMCheckerBuilder

settings_router = APIRouter(prefix="/settings", tags=["messages"])


@settings_router.get(
    "/llm",
    response_model=LLMSettingsResponse,
    responses={
        HTTPStatus.OK: {
            "description": "Successfully return LLM settings",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to find LLM settings",
        },
    },
)
async def get_llm_settings(
    settings_repo: Annotated[SettingsRepository, Depends(get_settings_repository)],
) -> LLMSettingsResponse:
    llm_settings_dict = await settings_repo.get_llm_settings()
    if llm_settings_dict is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Requested LLM settings were not found. Set the settings first",
        )
    return LLMSettingsResponse(**llm_settings_dict)


@settings_router.put("/llm")
async def post_user_message(
    llm_settings: LLMSettingsRequest,
    settings_repo: Annotated[SettingsRepository, Depends(get_settings_repository)],
) -> MessageResponse:
    await settings_repo.update_llm_settings(
        model_type=llm_settings.model_type,
        token=llm_settings.token,
        model_name=llm_settings.model_name,
        max_length=llm_settings.max_length,
    )
    return MessageResponse(message="LLM Settings updated successfully")


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
) -> LLMAvailabilityResponse:
    try:
        llm_checker = LLMCheckerBuilder.build(
            llm_settings.vendor, llm_settings.model, llm_settings.token, llm_settings.base_url
        )
    except NotImplementedError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Requested LLM type {llm_settings.model_type} was not found",
        ) from err
    is_available, error_message = await llm_checker.check()
    return LLMAvailabilityResponse(is_available=is_available, error_message=error_message)
