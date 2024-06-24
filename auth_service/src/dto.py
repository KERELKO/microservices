from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int | None = None
    username: str = ''
    password: str = ''
    token: str = ''
    email: str = ''
