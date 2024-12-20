from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

from src.config import app_config


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


# Before all models
metadata = SQLModel.metadata
engine = create_engine(url=app_config.sync_db_url, echo=True)
metadata.create_all(engine)
