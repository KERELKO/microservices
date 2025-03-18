import typing as t
from dataclasses import dataclass


type ID = int


class ReadableUser(t.TypedDict):
    id: ID
    username: str
    email: str | None


@dataclass
class User:
    id: ID
    username: str
    email: str | None = None
    password: str | None = None

    def for_reading(self) -> ReadableUser:
        return ReadableUser(id=self.id, username=self.username, email=self.email)
