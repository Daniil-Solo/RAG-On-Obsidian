from pydantic import BaseModel, Field


class BaseLLMSettings(BaseModel):
    vendor: str = Field(examples=["gigachat"])
    model: str = Field(examples=["GigaChat-Pro"])
    token: str = Field(examples=["3fs3sdfa0ikdadk3"])
    base_url: str = Field(examples=["https://gigachat.devices.sberbank.ru"])
    max_tokens: int = Field(examples=[2048])


class LLMSettingsRequest(BaseLLMSettings):
    ...


class LLMSettingsResponse(BaseLLMSettings):
    ...


class LLMAvailabilityResponse(BaseModel):
    is_available: bool
    error_message: str
