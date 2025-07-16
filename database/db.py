from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import get_settings
from .models import Base

settings = get_settings()

engine = create_async_engine(settings.db.dsn, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
