from dataclasses import asdict
from pydantic import BaseModel as Schema, Field

from .models import Product


class ProductSchema(Schema):
    id: str = ''
    title: str = ''
    price: float = 0.0
    description: str = ''
    tags: list[str] = Field(default_factory=list, kw_only=True)

    @classmethod
    def from_model(cls, product: Product) -> 'ProductSchema':
        return cls(**asdict(product))


class UserSchema(Schema):
    id: int | None = None
    username: str = ''
    email: str = ''
