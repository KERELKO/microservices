class ServiceException(Exception):
    ...


class AuthServiceException(Exception):
    def __init__(self, msg: str, *args) -> None:
        self.msg = msg
        self.args = args

    def __str__(self) -> str:
        return f'{self.msg}: {self.args}'
