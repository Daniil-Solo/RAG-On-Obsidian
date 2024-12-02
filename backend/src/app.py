from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.messages.router import messages_router
from src.api.settings.router import settings_router
from src.config import app_config
from src.utils.fastapi_docs import add_custom_docs_endpoints


def add_cors(application: FastAPI) -> None:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_routers(application: FastAPI, prefix: str = "") -> None:
    application.include_router(messages_router, prefix=prefix)
    application.include_router(settings_router, prefix=prefix)


def create_application() -> FastAPI:
    """Create FastAPI-application.

    :return: FastAPI
    """
    application = FastAPI(
        title="RAG on Obsidian",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
    )
    if app_config.is_debug:
        add_custom_docs_endpoints(application)
    add_cors(application)
    add_routers(application, prefix="/api")
    return application


app = create_application()
