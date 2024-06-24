import os
from dataclasses import dataclass


@dataclass(eq=False, repr=False, slots=True, frozen=True)
class Config:
    DEBUG: bool = True

    POSTGRES_DIALECT: str = 'postgresql+asyncpg'
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'postgres')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'postgres')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'db')

    @property
    def postgres_uri(self) -> str:
        user_pwd = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        host_port = f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}'
        connection_string = f'{self.POSTGRES_DIALECT}://{user_pwd}@{host_port}/{self.POSTGRES_DB}'
        return connection_string


config = Config()
