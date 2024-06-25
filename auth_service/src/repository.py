from dataclasses import asdict

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.db import User
from src.dto import UserDTO


class UserRepository:
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session: AsyncSession = session_factory()

    async def add(self, user: UserDTO) -> None:
        self.session.add(User(**asdict(user)))
        await self.session.commit()

    async def get(self, id: int) -> UserDTO | None:
        stmt = sql.select(User).where(User.id == id)
        user: User | None = await self.session.execute(stmt)  # type: ignore
        return user.to_dto() if user else None
