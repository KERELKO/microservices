from abc import ABC, abstractmethod
from dataclasses import dataclass

from .entities import User


@dataclass
class StoredUser:
    id: int
    username: str
    email: str | None = None
    hashed_password: str | None = None

    def as_user(self) -> User:
        return User(id=self.id, username=self.username, email=self.email)


class UserStorage(ABC):
    @abstractmethod
    async def add(self, user: StoredUser) -> int:
        ...

    @abstractmethod
    async def get(self, id: int) -> StoredUser | None:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> StoredUser | None:
        ...
