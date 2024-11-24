from pydantic import BaseModel, Field


class BaseLLMSettings(BaseModel):
    model_type: str = Field(examples=["gigachat"])
    token: str
    model_name: str = Field(examples=["GigaChat-Pro"])
    max_length: int = Field(examples=[2048])

class LLMSettingsRequest(BaseLLMSettings): ...


class LLMSettingsResponse(BaseLLMSettings): ...


class LLMAvailabilityResponse(BaseModel):
    is_available: bool
