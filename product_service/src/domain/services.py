from abc import ABC, abstractmethod

from .entities import Product


class ServiceException(Exception):
    ...


class AbstractProductService(ABC):
    @abstractmethod
    async def get_list(self, offset: int = 0, limit: int = 20) -> list[Product]:
        ...

    @abstractmethod
    async def create(self, entity: Product) -> None:
        ...

    @abstractmethod
    async def get_by_id(self, id: str) -> Product | None:
        ...
