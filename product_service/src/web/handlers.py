from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, status

from src.services.base import AbstractAuthService, AbstractProductService
from src.common.container import Container
from src.common.dto import Product

from .schemas import ProductSchema, UserSchema, Response


router = APIRouter(prefix='/v1/products', tags=['products'])


async def get_current_user(token: Annotated[str | None, Cookie()] = None) -> UserSchema:
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    service: AbstractAuthService = Container.resolve(AbstractAuthService)
    try:
        user = await service.get_user_by_token(token=token)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return UserSchema(**asdict(user))


@router.get('', response_model=Response[list[ProductSchema]])
async def get_product_list(
    offset: int,
    limit: int,
    user: Annotated[UserSchema, Depends(get_current_user)],
) -> Response[list[ProductSchema]]:
    service = Container.resolve(AbstractProductService)
    products: list[Product] = await service.get_list(offset=offset, limit=limit)
    return Response(data=[ProductSchema.from_dto(product) for product in products])


@router.post('', response_model=Response[None])
async def create_product(
    product: ProductSchema,
    user: Annotated[UserSchema, Depends(get_current_user)],
) -> Response[None]:
    service = Container.resolve(AbstractProductService)
    await service.create(Product(**product.model_dump()))
    return Response(data=None)
