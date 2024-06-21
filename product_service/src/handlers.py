from fastapi import APIRouter

from src.services.impl import ProductService

from .schemas import ProductSchema
from .models import Product


router = APIRouter(prefix='/products', tags=['products'])


@router.get('', response_model=list[ProductSchema])
async def get_products_list_handler(offset: int = 0, limit: int = 20) -> list[ProductSchema]:
    service = ProductService()
    products: list[Product] = await service.get_list(offset=offset, limit=limit)
    return [ProductSchema.from_model(product) for product in products]


@router.post('', response_model=dict[str, str])
async def create_product(product: ProductSchema) -> dict[str, str]:
    service = ProductService()
    await service.create(Product(**product.model_dump()))
    return {'status': 'OK'}
