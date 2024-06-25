from dataclasses import asdict

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from auth_service.src.storages.db import User, async_session_factory
from auth_service.src.dto.domain import UserSecureDTO, UserReadDTO

from .base import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def __init__(self, session_factory: async_sessionmaker = async_session_factory) -> None:
        self.session: AsyncSession = session_factory()

    async def add(self, dto: UserSecureDTO) -> UserReadDTO:
        sqlalchemy_model = User(**asdict(dto))
        self.session.add(sqlalchemy_model)
        await self.session.commit()
        return UserReadDTO(username=dto.username, email=dto.email, id=sqlalchemy_model.id)

    # TODO: try: return user and user.to_dto()
    async def get(self, id: int) -> UserSecureDTO | None:
        stmt = sql.select(User).where(User.id == id)
        user: User | None = await self.session.execute(stmt)  # type: ignore
        return user.to_dto() if user else None

    async def get_by_username(self, username: str) -> UserSecureDTO | None:
        stmt = sql.select(User).where(User.username == username)
        user: User | None = await self.session.execute(stmt)  # type: ignore
        return user.to_dto() if user else None
