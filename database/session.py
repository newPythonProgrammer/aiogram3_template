from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from database.db import async_session


@asynccontextmanager
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
