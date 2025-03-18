from mongorepo import implements  # type: ignore[import-untyped]
from mongorepo.implements.methods import (  # type: ignore[import-untyped]
    AddMethod, GetListMethod, GetMethod,
)

from src.common.config import get_conf
from src.common.dto import Product

from .base import AbstractRepository as ARepo


@implements(
    ARepo,
    GetMethod(ARepo.get, filters=['id']),
    AddMethod(ARepo.create, dto='entity'),
    GetListMethod(ARepo.get_list, filters=[], offset='offset', limit='limit'),
)
class ProductMongoRepository:
    class Meta:
        dto = Product
        id_field = 'id'
        collection = get_conf().get_async_mongo_client()['products_db']['products']
