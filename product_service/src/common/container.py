from functools import cache

import punq  # type: ignore[import-untyped]

from src.repositories.base import AbstractRepository
from src.repositories.mongo import ProductMongoRepository
from src.services.base import AbstractAuthService, AbstractProductService
from src.services.impl import ProductService, gRPCAuthService, RabbitAuthService  # noqa


class Container:
    def __init__(self, punq_container: punq.Container | None = None) -> None:
        self.punq_container = punq_container or self._init()

    def resolve[T](self, base_cls: type[T]) -> T:
        return self.punq_container.resolve(base_cls)  # type: ignore

    @classmethod
    def _init(cls) -> punq.Container:
        container = punq.Container()
        container.register(AbstractRepository, ProductMongoRepository)
        container.register(AbstractProductService, ProductService)

        # can be substituted with `FakeAuthService`, `RabbitAuthService` or `gRPCAuthService`
        container.register(AbstractAuthService, instance=gRPCAuthService())

        return container


@cache
def build_container() -> Container:
    return Container()
