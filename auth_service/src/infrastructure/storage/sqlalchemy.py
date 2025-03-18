import sqlalchemy as sa
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.db.sqlalchemy.config import async_session_factory
from src.infrastructure.db.sqlalchemy.models import user_table
from src.domain.storage import StoredUser, UserStorage


class SQLAlchemyUserStorage(UserStorage):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] = async_session_factory,
    ) -> None:
        self.session_factory = session_factory

    async def add(self, user: StoredUser) -> int:
        async with self.session_factory() as session:
            user.id = None  # type: ignore
            session.add(user)
            await session.commit()
            return user.id

    async def get(self, id: int) -> StoredUser | None:
        async with self.session_factory() as session:
            stmt = sa.select(StoredUser).where(user_table.c['id'] == id)
            user: StoredUser | None = (await session.execute(stmt)).scalar_one_or_none()
            return user if user else None

    async def get_by_username(self, username: str) -> StoredUser | None:
        async with self.session_factory() as session:
            stmt = sa.select(StoredUser).where(user_table.c['username'] == username)
            user: StoredUser | None = (await session.execute(stmt)).scalar_one_or_none()
            return user if user else None
