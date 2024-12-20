from enum import Enum
from typing import Optional
from pydantic import DirectoryPath, Field, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationMode(Enum):
    DEBUG = "debug"
    PRODUCTION = "production"
    TEST = "test"


class ApplicationConfig(BaseSettings):
    OBSIDIAN_PATH: str = DirectoryPath()
    MODE: ApplicationMode = Field(default=ApplicationMode.DEBUG)
    DB_PATH: str = Field(default="./rag_on_obsidian.db")
    ORIGINS: str = Field(default="")
    STATIC_PATH: Optional[str] = Field(default=None)
    QDRANT_URL: str = Field()

    @property
    def is_debug(self) -> bool:
        return self.MODE == ApplicationMode.DEBUG

    @property
    def sync_db_url(self) -> str:
        return f"sqlite:///{self.DB_PATH}"

    @property
    def async_db_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.DB_PATH}"

    @property
    def origins(self) -> list[str]:
        return [origin for origin in self.ORIGINS.split(",") if origin != ""]

    model_config = SettingsConfigDict(env_file=".env")


app_config = ApplicationConfig()
