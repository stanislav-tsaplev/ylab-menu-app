from os import getenv

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


db_engine = create_async_engine(DB_URL)


async def init_db() -> None:
    async with db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def async_session() -> AsyncSession:
    async with AsyncSession(db_engine) as session:
        yield session
