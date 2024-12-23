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
    DB_HOST: str = Field()
    DB_PORT: int = Field()
    DB_USER: str = Field()
    DB_PASSWORD: str = Field()
    DB_NAME: str = Field()
    ORIGINS: str = Field(default="")
    STATIC_PATH: Optional[str] = Field(default=None)
    QDRANT_URL: Optional[str] = Field(default=None)

    @property
    def is_debug(self) -> bool:
        return self.MODE == ApplicationMode.DEBUG

    @property
    def sync_db_url(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def async_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def origins(self) -> list[str]:
        return [origin for origin in self.ORIGINS.split(",") if origin != ""]

    model_config = SettingsConfigDict(env_file=".env")


app_config = ApplicationConfig()
