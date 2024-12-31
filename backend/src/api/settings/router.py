from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.api.general_dependencies import get_llm_tokens_repository
from src.api.general_schemas import MessageResponse
from src.api.settings.dependencies import get_settings_repository
from src.api.settings.schemas import LLMAvailabilityResponse, LLMSettingsRequest, LLMSettingsResponse
from src.repositories.llm_tokens.interface import LLMTokensRepository
from src.repositories.settings.interface import SettingsRepository
from src.services.llm_service.builder import LLMServiceBuilder

settings_router = APIRouter(prefix="/settings", tags=["settings"])


@settings_router.get(
    "/llm/",
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


@settings_router.put("/llm/")
async def post_user_message(
    llm_settings: LLMSettingsRequest,
    settings_repo: Annotated[SettingsRepository, Depends(get_settings_repository)],
llm_tokens_repository: Annotated[LLMTokensRepository, Depends(get_llm_tokens_repository)],
) -> MessageResponse:
    await settings_repo.update_llm_settings(
        vendor=llm_settings.vendor,
        token=llm_settings.token,
        model=llm_settings.model,
        base_url=llm_settings.base_url,
        max_tokens=llm_settings.max_tokens,
    )
    await llm_tokens_repository.clean()
    return MessageResponse(message="LLM Settings updated successfully")


@settings_router.post(
    "/llm/checking/",
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
        llm_service = LLMServiceBuilder.build(
            llm_settings.vendor, llm_settings.model, llm_settings.token, llm_settings.base_url, llm_settings.max_tokens
        )
    except NotImplementedError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Requested LLM type {llm_settings.vendor} was not found",
        ) from err
    is_available, error_message = await llm_service.check()
    return LLMAvailabilityResponse(is_available=is_available, error_message=error_message)
