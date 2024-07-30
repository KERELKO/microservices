from typing import Any

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.common.dto import UserSecureDTO


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
