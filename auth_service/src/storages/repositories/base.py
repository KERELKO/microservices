from abc import ABC, abstractmethod

from auth_service.src.dto.domain import UserSecureDTO, UserReadDTO


class AbstractUserRepository(ABC):
    @abstractmethod
    async def add(self, user: UserSecureDTO) -> UserReadDTO:
        ...

    @abstractmethod
    async def get(self, id: int) -> UserSecureDTO | None:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> UserSecureDTO | None:
        ...
