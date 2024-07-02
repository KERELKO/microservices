from typing import NoReturn

import bcrypt


def raise_exc(exc: Exception) -> NoReturn:
    raise exc


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()
