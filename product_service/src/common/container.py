from functools import cache
from typing import Any, Type, TypeVar

import punq

from src.repositories.base import AbstractRepository
from src.repositories.mongo import ProductMongoRepository
from src.services.base import AbstractAuthService, AbstractProductService
from src.services.impl import ProductService, RabbitAuthService, gRPCAuthService  # noqa


ABC = TypeVar('ABC')


class Container:
    @classmethod
    @cache
    def get(cls) -> punq.Container:
        return cls.__init()

    @staticmethod
    def resolve(base_cls: Type[ABC]) -> Any:
        return Container.get().resolve(base_cls)

    @classmethod
    def __init(cls) -> punq.Container:
        container = punq.Container()
        container.register(AbstractRepository, ProductMongoRepository)
        container.register(AbstractProductService, ProductService)
        container.register(AbstractAuthService, instance=gRPCAuthService())
        return container
