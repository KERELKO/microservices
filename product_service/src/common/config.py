from functools import cache

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    MONGO_DB_HOST: str = Field(default='mongodb')
    MONGO_DB_PORT: int = Field(default=27017)

    RMQ_HOST: str = Field(default='rabbitmq')
    RMQ_PORT: int = Field(default=5672)

    gRPC_HOST: str = Field(default='auth-app')
    gRPC_PORT: int = Field(default=50051)

    @property
    def grpc_url(self) -> str:
        return f'{self.gRPC_HOST}:{self.gRPC_PORT}'

    @property
    def mongodb_connection_string(self) -> str:
        return f'mongodb://{self.MONGO_DB_HOST}:{self.MONGO_DB_PORT}/'

    @property
    def rabbitmq_connection_string(self) -> str:
        return f'rabbitmq://{self.RMQ_HOST}:{self.RMQ_PORT}/'

    def get_async_mongo_client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(host=self.MONGO_DB_HOST, port=int(self.MONGO_DB_PORT))


@cache
def get_conf() -> Config:
    return Config()  # type: ignore
