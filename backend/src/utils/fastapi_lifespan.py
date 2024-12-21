from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config import app_config
from src.services.rag_service.demo import DemoQdrantRagService
from src.database.scripts import create_database


@asynccontextmanager
async def lifespan(application: FastAPI):
    create_database(app_config.sync_db_url)
    if app_config.QDRANT_URL:
        rag_service = DemoQdrantRagService(qdrant_url=app_config.QDRANT_URL)
        await rag_service.create_vectordb(app_config.OBSIDIAN_PATH)
    yield
