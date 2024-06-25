from dataclasses import dataclass


@dataclass
class UserReadDTO:
    id: int | None = None
    username: str = ''
    email: str = ''


@dataclass
class UserDTO:
    id: int | None = None
    username: str = ''
    password: str = ''
    email: str = ''


@dataclass
class UserSecureDTO:
    id: int | None = None
    username: str = ''
    email: str = ''
    hashed_password: str = ''
