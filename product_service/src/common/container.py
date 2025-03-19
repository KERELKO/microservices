from functools import cache

import punq  # type: ignore[import-untyped]

from src.domain.services import AbstractProductService
from src.infrastructure.services.mongo import ProductMongoService
from src.infrastructure.services.auth import AbstractAuthService, FakeAuthService  # noqa
from src.infrastructure.services.auth.grpc import GRPCAuthService
from src.infrastructure.services.auth.rmq import RabbitAuthService  # noqa


class Container:
    def __init__(self, punq_container: punq.Container | None = None) -> None:
        self.punq_container = punq_container or self._init()

    def resolve[T](self, base_cls: type[T]) -> T:
        return self.punq_container.resolve(base_cls)  # type: ignore

    @classmethod
    def _init(cls) -> punq.Container:
        container = punq.Container()
        container.register(AbstractProductService, ProductMongoService)

        # can be substituted with `FakeAuthService`, `RabbitAuthService` or `gRPCAuthService`
        container.register(AbstractAuthService, instance=GRPCAuthService())

        return container


@cache
def build_container() -> Container:
    return Container()
