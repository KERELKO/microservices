from mongorepo import Access
from mongorepo.asyncio.decorators import async_mongo_repository

from src.config import config
from src.models import Product


@async_mongo_repository(method_access=Access.PROTECTED)
class ProductMongoRepository:
    class Meta:
        dto = Product
        id_field = 'id'
        collection = config.get_async_mongo_client()['product_db']['products_1']

    async def get_products(self) -> list[Product]:
        products = list(await self.get_all())  # type: ignore
        return products

    async def create_product(self, product: Product) -> None:
        await self._add(product)  # type: ignore
