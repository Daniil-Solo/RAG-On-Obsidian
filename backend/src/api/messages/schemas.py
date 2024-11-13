from datetime import datetime

from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    id: int = Field(examples=[1])
    role: str = Field(examples=["user"])
    content: str = Field(examples=["Какой язык стоит учить после Python?"])
    created_date: datetime


class MessageHistoryResponse(BaseModel):
    messages: list[MessageSchema]


class QueryRequest(BaseModel):
    content: str = Field(examples=["Какой язык стоит учить после Python?"])


class AnswerResponse(BaseModel):
    answer: str = Field(examples=["Конечно же C++"])
    related_documents: list[str] = Field(examples=[["C++.md", "Python vs C++.md"]])
