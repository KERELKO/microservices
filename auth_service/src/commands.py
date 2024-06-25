from dataclasses import dataclass


@dataclass(eq=False, repr=False)
class Command:
    command: str


@dataclass
class RegisterUser(Command):
    username: str
    password: str
    email: str = ''
