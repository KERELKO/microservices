from typing import NoReturn


def raise_exc(exc: Exception) -> NoReturn:
    raise exc


class DomainException(Exception):
    ...


class IncorrectCredentialsException(DomainException):
    ...
