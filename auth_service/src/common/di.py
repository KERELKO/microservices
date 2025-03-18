from functools import cache

import punq  # type: ignore[import-untyped]

from src.common.config import Config, get_conf

from src.infrastructure.storage.sqlalchemy import SQLAlchemyUserStorage

from src.domain.service import AuthService
from src.domain.storage import UserStorage


class Container:
    def __init__(self, punq_container: punq.Container | None = None) -> None:
        self.punq_container = punq_container or self._init()

    def resolve[T](self, base_cls: type[T]) -> T:
        return self.punq_container.resolve(base_cls)  # type: ignore

    @classmethod
    def _init(cls) -> punq.Container:
        container = punq.Container()

        config = get_conf()
        container.register(Config, instance=config)
        storage = SQLAlchemyUserStorage()
        container.register(UserStorage, factory=SQLAlchemyUserStorage)
        container.register(
            AuthService,
            instance=AuthService(
                storage=storage,
                crypto_context=config.crypto_context,
                access_token_expire_minutes=config.access_token_expire_minutes,
                secret_key=config.secret_key,
                algorithm=config.algorithm,
            )
        )

        return container


@cache
def build_container() -> Container:
    return Container()
