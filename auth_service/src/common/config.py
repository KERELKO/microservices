from functools import cache

from pydantic_settings import BaseSettings
from pydantic import Field

from passlib.context import CryptContext  # type: ignore


class Config(BaseSettings):
    debug: bool = True

    postgres_dialect: str = 'postgresql+asyncpg'
    postgres_port: int = Field(alias='POSTGRES_PORT')
    postgres_host: str = Field(alias='POSTGRES_HOST')
    postgres_user: str = Field(alias='POSTGRES_USER')
    postgres_password: str = Field(alias='POSTGRES_PASSWORD')
    postgres_db: str = Field(alias='POSTGRES_DB')

    rabbitmq_host: str = Field(alias='RABBITMQ_HOST')
    rabbitmq_port: int = Field(alias='RABBITMQ_PORT')

    secret_key: str = Field(alias='SECRET_KEY')
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = Field(alias='ACCESS_TOKEN_EXPIRE_MINUTES', default=30)
    crypto_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @property
    def postgres_uri(self) -> str:
        user_pwd = f'{self.postgres_user}:{self.postgres_password}'
        host_port = f'{self.postgres_host}:{self.postgres_port}'
        connection_string = f'{self.postgres_dialect}://{user_pwd}@{host_port}/{self.postgres_db}'
        return connection_string


@cache
def get_conf() -> Config:
    return Config()  # type: ignore[call-arg]
