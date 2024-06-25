from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

from auth_service.src.dto.domain import UserSecureDTO
from src.config import config


engine = create_async_engine(config.postgres_uri)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)


def init_tables():
    import asyncio

    async def create_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(create_db())


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(40), default='')

    def __repr__(self) -> str:
        return f'User(id={self.id} username={self.username} email={self.email})'

    def as_dict(self) -> dict[str, Any]:
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'hashed_password': self.hashed_password
        }
        return data

    def to_dto(self) -> UserSecureDTO:
        return UserSecureDTO(**self.as_dict())
