from typing import Annotated

from fastapi import APIRouter, Depends

from src.services.base import AbstractProductService
from src.common.dto import Product

from .utils import get_current_user
from .schemas import ProductSchema, UserOut, Response
from . import ContainerDep

router = APIRouter(prefix='/v1/products', tags=['products'])


@router.get('', response_model=Response[list[ProductSchema]])
async def get_product_list(
    offset: int,
    limit: int,
    container: ContainerDep,
    user: Annotated[UserOut, Depends(get_current_user)],
) -> Response[list[ProductSchema]]:
    service: AbstractProductService = container.resolve(AbstractProductService)  # type: ignore
    products: list[Product] = await service.get_list(offset=offset, limit=limit)
    return Response(data=[ProductSchema.from_dto(product) for product in products])


@router.post('', response_model=Response[None])
async def create_product(
    product: ProductSchema,
    container: ContainerDep,
    user: Annotated[UserOut, Depends(get_current_user)],
) -> Response[None]:
    service = container.resolve(AbstractProductService)  # type: ignore
    await service.create(Product(**product.model_dump()))
    return Response(data=None)
