from pydantic import BaseModel, Field


class LLMTokensResponse(BaseModel):
    input_tokens: int = Field(examples=[3242])
    output_tokens: int = Field(examples=[253256])
