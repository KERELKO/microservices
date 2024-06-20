from fastapi import APIRouter

from .schemas import ProductSchema
from .service import Service
from .models import Product


router = APIRouter(prefix='/products', tags=['products'])


@router.get('', response_model=list[ProductSchema])
async def get_all_products_handler() -> list[ProductSchema]:
    service = Service()
    products: list[Product] = await service.get_all_products()
    return [ProductSchema.from_model(product) for product in products]
