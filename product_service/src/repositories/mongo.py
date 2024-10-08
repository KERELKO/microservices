# type: ignore[reportAttributeAccessIssue]
from mongorepo import Access
from mongorepo.asyncio.decorators import async_mongo_repository

from src.common.config import get_conf
from src.common.dto import Product

from .base import AbstractRepository


@async_mongo_repository(method_access=Access.PROTECTED)
class ProductMongoRepository(AbstractRepository[Product]):
    class Meta:
        dto = Product
        id_field = 'id'
        collection = get_conf().get_async_mongo_client()['products_db']['products']

    async def get(self, id: str) -> Product | None:
        entity = await self._get(id=id)
        return entity

    async def create(self, entity: Product) -> None:
        await self._add(entity)

    async def get_list(self, offset: int = 0, limit: int = 20) -> list[Product]:
        return await self._get_list(offset=offset, limit=limit)
