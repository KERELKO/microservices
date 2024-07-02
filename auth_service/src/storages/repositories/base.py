from abc import ABC, abstractmethod

from src.common.dto import UserSecureDTO


class AbstractUserRepository(ABC):
    @abstractmethod
    async def add(self, user: UserSecureDTO) -> UserSecureDTO:
        ...

    @abstractmethod
    async def get(self, id: int) -> UserSecureDTO | None:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> UserSecureDTO | None:
        ...
