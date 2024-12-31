from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.types import Lifespan

from src.config import app_config
from src.database.scripts import create_database


@asynccontextmanager
async def lifespan(application: FastAPI) -> Lifespan:  # noqa: ARG001
    create_database(app_config.sync_db_url)
    yield
