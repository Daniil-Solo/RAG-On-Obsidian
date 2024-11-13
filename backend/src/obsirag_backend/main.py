from fastapi import FastAPI

from obsirag_backend.api.messages.routes import router as messages_router

app = FastAPI(title="Obsidian RAG Backend")

app.include_router(messages_router)
