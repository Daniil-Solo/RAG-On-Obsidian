from datetime import datetime
from typing import Optional, Any

from pgvector.sqlalchemy import Vector
from sqlmodel import Field, SQLModel
from sqlalchemy import Column


class MessageModel(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(..., nullable=False)
    role: str = Field(..., nullable=False)
    created_date: datetime = Field(default_factory=datetime.utcnow)


class LLMSettingsModel(SQLModel, table=True):
    __tablename__ = "llm_settings"

    id: int = Field(default=None, primary_key=True)
    vendor: str = Field(..., nullable=False)
    model: str = Field(..., nullable=False)
    base_url: str = Field(..., nullable=False)
    token: str = Field(..., nullable=False)
    max_tokens: int = Field(..., nullable=False)


class FileModel(SQLModel, table=True):
    __tablename__ = "files"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., nullable=False)
    size: int = Field(..., nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    x: float = Field(..., nullable=False)
    y: float = Field(..., nullable=False)


class UpdateProcessModel(SQLModel, table=True):
    __tablename__ = "update_process"

    id: Optional[int] = Field(default=None, primary_key=True)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = Field(default=None)
    is_actual: bool = Field(default=True)


class ProgressStageModel(SQLModel, table=True):
    __tablename__ = "progress_stage"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., nullable=False)
    process_id: int = Field(..., nullable=False)
    progress: int = Field(..., nullable=False)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = Field(default=None)


class LLMTokensModel(SQLModel, table=True):
    __tablename__ = "llm_tokens"

    id: int = Field(default=None, primary_key=True)
    input_tokens: int = Field(default=0, nullable=False)
    output_tokens: int = Field(default=0, nullable=False)


class ChunkEmbeddingModel(SQLModel, table=True):
    __tablename__ = "chunk_embeddings"

    id: int = Field(default=None, primary_key=True)
    filename: str = Field(..., nullable=False)
    text: str = Field(..., nullable=False)
    embedding: Any = Field(sa_column=Column(Vector(1024)))
