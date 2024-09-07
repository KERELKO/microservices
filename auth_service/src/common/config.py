from functools import cache

from pydantic_settings import BaseSettings

from passlib.context import CryptContext


class Config(BaseSettings):
    DEBUG: bool = True

    POSTGRES_DIALECT: str = 'postgresql+asyncpg'
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CRYPTO_CONTEXT: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @property
    def postgres_uri(self) -> str:
        user_pwd = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        host_port = f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}'
        connection_string = f'{self.POSTGRES_DIALECT}://{user_pwd}@{host_port}/{self.POSTGRES_DB}'
        return connection_string


@cache
def get_conf() -> Config:
    return Config()  # type: ignore[reportCallIssue]
