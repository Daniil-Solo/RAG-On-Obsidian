from sqlmodel import create_engine
from src.database.models import SQLModel


def create_database(sync_db_url: str, echo=True) -> None:
    metadata = SQLModel.metadata
    engine = create_engine(url=sync_db_url, echo=echo)
    metadata.create_all(engine)
