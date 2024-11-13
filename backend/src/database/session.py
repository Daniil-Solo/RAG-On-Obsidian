from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import app_config

async_engine = create_async_engine(url=app_config.async_db_url, echo=app_config.is_debug)
async_session_factory = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
