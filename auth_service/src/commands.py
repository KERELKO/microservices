from dataclasses import dataclass


class Command:
    ...


@dataclass
class RegisterUser(Command):
    username: str
    password: str
    email: str = ''
