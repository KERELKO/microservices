from dataclasses import dataclass, field


@dataclass
class Product:
    id: str
    title: str = ''
    price: float = 0.0
    description: str = ''
    tags: list[str] = field(default_factory=list, kw_only=True)


@dataclass
class User:
    id: str = ''
    username: str = ''
    password: str = ''
    token: str = ''
