from collections.abc import AsyncGenerator

from asyncpg import Connection
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from config.settings import settings
from src.logger import logger


def create_db_engine() -> AsyncEngine:
    logger.info('Creating database engine')
    return create_async_engine(
        settings.db_url,
        poolclass=AsyncAdaptedQueuePool,
        connect_args={
            'connection_class': Connection,
        },
    )


def create_db_session(_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    logger.info('Creating database session')
    return async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


engine = create_db_engine()
async_session = create_db_session(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    logger.info('Getting database session')
    async with async_session() as session:
        yield session
    logger.info('Database session closed')
