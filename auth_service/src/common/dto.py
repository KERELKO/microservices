from dataclasses import dataclass


@dataclass(eq=False)
class UserReadDTO:
    id: int | None = None
    username: str = ''
    email: str = ''


@dataclass(eq=False)
class UserInputDTO:
    id: int | None = None
    username: str = ''
    password: str = ''
    email: str = ''


@dataclass(eq=False)
class UserSecureDTO:
    id: int | None = None
    username: str = ''
    hashed_password: str = ''
    email: str = ''
