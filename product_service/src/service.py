from .models import Product


class Service:
    async def get_all_products(self) -> list[Product]:
        ...
