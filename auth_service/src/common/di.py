from functools import cache
from typing import Any, Type, TypeVar

import punq

from src.storages.repositories.base import AbstractUserRepository
from src.storages.repositories.impl import SQLAlchemyUserRepository
from src.services.auth import AuthService


BaseClass = TypeVar('BaseClass')


class Container:
    @classmethod
    def get(cls) -> punq.Container:
        return cls.__init()

    @staticmethod
    def resolve(base_cls: Type[BaseClass]) -> Any:
        return Container.get().resolve(base_cls)

    @classmethod
    @cache
    def __init(cls) -> punq.Container:
        container = punq.Container()

        container.register(AbstractUserRepository, SQLAlchemyUserRepository)
        container.register(AuthService)

        return container
