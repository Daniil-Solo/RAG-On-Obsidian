from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors(application: FastAPI, origins: list[str]) -> None:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
