from dataclasses import asdict

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import exc

from src.common.db.sqlalchemy.models import User
from src.common.db.sqlalchemy.config import async_session_factory
from src.common.dto import UserSecureDTO

from .base import AbstractUserRepository


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session_factory: async_sessionmaker = async_session_factory) -> None:
        self.session_factory = session_factory

    async def add(self, dto: UserSecureDTO) -> UserSecureDTO:
        async with self.session_factory() as session:
            sqlalchemy_model = User(**asdict(dto))
            session.add(sqlalchemy_model)
            await session.commit()
            dto.id = sqlalchemy_model.id
            return dto

    async def get(self, id: int) -> UserSecureDTO | None:
        async with self.session_factory() as session:
            stmt = sql.select(User).where(User.id == id)
            try:
                user: User | None = (await session.execute(stmt)).scalar_one()
            except exc.NoResultFound:
                return None
            return user.to_dto() if user else None

    async def get_by_username(self, username: str) -> UserSecureDTO | None:
        async with self.session_factory() as session:
            stmt = sql.select(User).where(User.username == username)
            try:
                user: User | None = (await session.execute(stmt)).scalar_one()
            except exc.NoResultFound:
                return None
            return user.to_dto() if user else None
