from abc import ABC, abstractmethod


class AbstractAuthService[T](ABC):
    @abstractmethod
    async def get_user_by_token(self, token: str) -> T:
        ...


class AuthServiceException(Exception):
    def __init__(self, msg: str, *args) -> None:
        self.msg = msg
        self.args = args

    def __str__(self) -> str:
        return f'{self.msg}: {self.args}'
