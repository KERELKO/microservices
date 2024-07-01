from typing import Annotated, Any

from fastapi import APIRouter, Cookie, Depends, HTTPException

from src.services.impl import ProductService, RPCAuthClient

from .schemas import ProductSchema, UserSchema
from .models import Product


router = APIRouter(prefix='/products', tags=['products'])


def get_current_user(token: Annotated[str | None, Cookie()] = None) -> UserSchema:
    if not token:
        raise HTTPException(401)
    service = RPCAuthClient()
    response = service.call({'token': token})

    if response['meta']['errors']:
        raise HTTPException(403)

    if response['data'] is not None:
        u = response['data']
        user = UserSchema(id=u['id'], username=u['username'], email=u['email'])

    return user


@router.get('', response_model=list[ProductSchema])
async def get_products_list(
    offset: int,
    limit: int,
    user: Annotated[str, Depends(get_current_user)],
) -> list[ProductSchema]:
    service = ProductService()
    products: list[Product] = await service.get_list(offset=offset, limit=limit)
    return [ProductSchema.from_model(product) for product in products]


@router.post('', response_model=dict[str, str])
async def create_product(product: ProductSchema) -> dict[str, str]:
    service = ProductService()
    await service.create(Product(**product.model_dump()))
    return {'status': 'OK'}


@router.get('/ping')
async def ping(token: Annotated[str, Cookie()]) -> dict[str, Any]:
    return {'token': token}
