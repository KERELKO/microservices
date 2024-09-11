from typing import Annotated

from fastapi import APIRouter, Depends

from src.services.base import AbstractProductService
from src.common.container import Container
from src.common.dto import Product

from .utils import get_current_user
from .schemas import ProductSchema, UserOut, Response


router = APIRouter(prefix='/v1/products', tags=['products'])


@router.get('', response_model=Response[list[ProductSchema]])
async def get_product_list(
    offset: int,
    limit: int,
    user: Annotated[UserOut, Depends(get_current_user)],
) -> Response[list[ProductSchema]]:
    service: AbstractProductService = Container.resolve(AbstractProductService)
    products: list[Product] = await service.get_list(offset=offset, limit=limit)
    return Response(data=[ProductSchema.from_dto(product) for product in products])


@router.post('', response_model=Response[None])
async def create_product(
    product: ProductSchema,
    user: Annotated[UserOut, Depends(get_current_user)],
) -> Response[None]:
    service: AbstractProductService = Container.resolve(AbstractProductService)
    await service.create(Product(**product.model_dump()))
    return Response(data=None)
