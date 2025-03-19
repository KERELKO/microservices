from typing import Annotated

from fastapi import APIRouter, Depends

from src.domain.entities import Product
from src.domain.services import AbstractProductService

from .utils import get_current_user_from_cookie_token
from .schemas import ProductSchema, UserOut, Response
from . import ContainerDep

router = APIRouter(prefix='/v1/products', tags=['products'])


@router.get('', response_model=Response[list[ProductSchema]])
async def get_product_list(
    offset: int,
    limit: int,
    container: ContainerDep,
    _: Annotated[UserOut, Depends(get_current_user_from_cookie_token)],
) -> Response[list[ProductSchema]]:
    service: AbstractProductService = container.resolve(AbstractProductService)  # type: ignore
    products: list[Product] = await service.get_list(offset=offset, limit=limit)
    return Response(data=[ProductSchema.from_dto(product) for product in products])


@router.post('', response_model=Response[None])
async def create_product(
    product: ProductSchema,
    container: ContainerDep,
    _: Annotated[UserOut, Depends(get_current_user_from_cookie_token)],
) -> Response[None]:
    service = container.resolve(AbstractProductService)  # type: ignore
    await service.create(Product(**product.model_dump()))
    return Response(data=None)
