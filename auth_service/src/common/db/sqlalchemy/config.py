from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.common.config import get_conf

from .models import Base


engine = create_async_engine(get_conf().postgres_uri)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)


def init_tables():
    import asyncio

    async def create_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(create_db())
