from sqlmodel import create_engine
from src.database.models import SQLModel
from src.database.indexes import embedding_index


def create_database(sync_db_url: str, echo=True) -> None:
    metadata = SQLModel.metadata
    engine = create_engine(url=sync_db_url, echo=echo)
    metadata.create_all(engine, checkfirst=True)
    embedding_index.create(engine, checkfirst=True)
