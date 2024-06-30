import os
from dataclasses import dataclass


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
    RMQ_PORT: int = int(os.getenv('RABBITMQ_PORT', 6379))

    SECRET_KEY: str = 'c32d7bb1aa31c88979d174470152f446eb98351e1ae3c9ccb594dcc413261ed4'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def postgres_uri(self) -> str:
        user_pwd = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        host_port = f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}'
        connection_string = f'{self.POSTGRES_DIALECT}://{user_pwd}@{host_port}/{self.POSTGRES_DB}'
        return connection_string


config = Config()
