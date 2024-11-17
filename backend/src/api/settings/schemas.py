from pydantic import BaseModel, Field


class LLMSettingsRequest(BaseModel):
    model_type: str = Field(examples=["gigachat"])
    token: str
    model_name: str = Field(examples=["GigaChat-Pro"])
    max_length: int = Field(examples=[2048])


class LLMSettingsResponse(BaseModel):
    model_type: str = Field(default="", examples=["gigachat"])
    token: str = Field(default="")
    model_name: str = Field(default="", examples=["GigaChat-Pro"])
    max_length: int = Field(default=2048, examples=[2048])
