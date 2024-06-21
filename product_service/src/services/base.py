from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar('T')


class AbstractService(Generic[T], ABC):
    @abstractmethod
    async def get_list(self, offset: int = 0, limit: int = 20) -> list[T]:
        ...

    @abstractmethod
    async def create(self, entity: T) -> None:
        ...

    @abstractmethod
    async def get_by_id(self, id: str) -> T | None:
        ...
