from mongorepo import implements  # type: ignore[import-untyped]
from mongorepo.implements.methods import (  # type: ignore[import-untyped]
    AddMethod, GetListMethod, GetMethod,
)

from src.common.config import get_conf

from src.domain.entities import Product
from src.domain.services import AbstractProductService


@implements(
    AbstractProductService,
    GetMethod(AbstractProductService.get_by_id, filters=['id']),
    AddMethod(AbstractProductService.create, dto='entity'),
    GetListMethod(AbstractProductService.get_list, filters=[], offset='offset', limit='limit'),
)
class ProductMongoService:
    class Meta:
        dto = Product
        id_field = 'id'
        collection = get_conf().get_async_mongo_client()['products_db']['products']
