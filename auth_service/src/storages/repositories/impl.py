from dataclasses import asdict

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import exc

from src.storages.db import User, async_session_factory
from src.dto.domain import UserSecureDTO, UserReadDTO

from .base import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def __init__(self, session_factory: async_sessionmaker = async_session_factory) -> None:
        self.session_factory = session_factory

    async def add(self, dto: UserSecureDTO) -> UserReadDTO:
        async with self.session_factory() as session:
            sqlalchemy_model = User(**asdict(dto))
            session.add(sqlalchemy_model)
            await session.commit()
            return UserReadDTO(username=dto.username, email=dto.email, id=sqlalchemy_model.id)

    async def get(self, id: int) -> UserSecureDTO | None:
        async with self.session_factory() as session:
            stmt = sql.select(User).where(User.id == id)
            user: User | None = (await session.execute(stmt)).scalar_one()
            return user.to_dto() if user else None

    async def get_by_username(self, username: str) -> UserSecureDTO | None:
        async with self.session_factory() as session:
            stmt = sql.select(User).where(User.username == username)
            try:
                user: User | None = (await session.execute(stmt)).scalar_one()
            except exc.NoResultFound:
                return None
            return user.to_dto() if user else None
