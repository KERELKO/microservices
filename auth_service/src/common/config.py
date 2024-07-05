import os
from functools import cache
from dataclasses import dataclass

from passlib.context import CryptContext


@dataclass(eq=False, repr=False, slots=True, frozen=True)
class Config:
    DEBUG: bool = True

    POSTGRES_DIALECT: str = 'postgresql+asyncpg'
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'db')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'postgres')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'db')

    RMQ_HOST: str = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    RMQ_PORT: int = int(os.getenv('RABBITMQ_PORT', 5672))

    SECRET_KEY: str = os.getenv('SECRET_KEY', 'secret_key')
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CRYPTO_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @property
    def postgres_uri(self) -> str:
        user_pwd = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        host_port = f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}'
        connection_string = f'{self.POSTGRES_DIALECT}://{user_pwd}@{host_port}/{self.POSTGRES_DB}'
        return connection_string


@cache
def get_conf() -> Config:
    return Config()
