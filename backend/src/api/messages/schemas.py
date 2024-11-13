from pydantic import BaseModel


class MessageResponse(BaseModel):
    role: str
    content: str
    datetime: str


class UserMessageRequest(BaseModel):
    content: str


class ModelMessageResponse(BaseModel):
    answer: str
    related_documents: list[str]
