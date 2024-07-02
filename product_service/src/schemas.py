from dataclasses import asdict
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

from .dto import Product


T = TypeVar('T')


class Response(BaseModel, Generic[T]):
    data: T
    status: str
    meta: dict[str, Any] = Field(default_factory=dict)


class ProductSchema(BaseModel):
    id: str = ''
    title: str = ''
    price: float = 0.0
    description: str = ''
    tags: list[str] = Field(default_factory=list, kw_only=True)

    @classmethod
    def from_dto(cls, product: Product) -> 'ProductSchema':
        return cls(**asdict(product))


class UserSchema(BaseModel):
    id: int | None = None
    username: str = ''
    email: str = ''
