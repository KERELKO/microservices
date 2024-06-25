from src.repositories.base import AbstractRepository
from src.repositories.mongo import ProductMongoRepository
from src.models import Product

from .base import AbstractService


class ProductService(AbstractService[Product]):
    def __init__(self, repository: AbstractRepository | None = None) -> None:
        self.repo = ProductMongoRepository()

    async def get_list(self, offset: int = 0, limit: int = 20) -> list[Product]:
        products = await self.repo.get_list(offset=offset, limit=limit)
        return products

    async def create(self, product: Product) -> None:
        await self.repo.create(product)

    async def get_by_id(self, id: str) -> Product | None:
        product = await self.repo.get(id=id)
        return product


class RMQUserService:
    def __init__(self, rmq_host: str, rmq_port: int) -> None:
        ...
