from sqlmodel import create_engine

from src.database.indexes import embedding_index
from src.database.models import SQLModel


def create_database(sync_db_url: str, *, echo: bool = True) -> None:
    metadata = SQLModel.metadata
    engine = create_engine(url=sync_db_url, echo=echo)
    metadata.create_all(engine, checkfirst=True)
    embedding_index.create(engine, checkfirst=True)
