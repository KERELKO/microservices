from functools import cache
from typing import Literal

from motor.motor_asyncio import AsyncIOMotorClient

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    mode: Literal['prod', 'dev', 'debug'] = Field(alias='MODE', default='debug')

    mongodb_host: str = Field(alias='MONGODB_HOST', default='mongodb')
    mongodb_port: int = Field(alias='MONGODB_PORT', default=27017)

    rabbitmq_host: str = Field(alias='RABBITMQ_HOST', default='rabbitmq')
    rabbitmq_port: int = Field(alias='RABBITMQ_PORT', default=5672)

    grpc_auth_host: str = Field(alias='GRPC_AUTH_HOST', default='auth-app')
    grpc_auth_port: int = Field(alias='GRPC_AUTH_HOST', default=50051)

    @property
    def profiling(self) -> bool:
        return True if self.mode in ['dev', 'debug'] else False

    @property
    def grpc_uri(self) -> str:
        return f'{self.grpc_auth_host}:{self.grpc_auth_port}'

    @property
    def mongodb_connection_string(self) -> str:
        return f'mongodb://{self.mongodb_host}:{self.mongodb_port}/'

    @property
    def rabbitmq_connection_string(self) -> str:
        return f'rabbitmq://{self.mongodb_host}:{self.mongodb_port}/'

    def get_async_mongo_client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(host=self.mongodb_host, port=int(self.mongodb_port))


@cache
def get_conf() -> Config:
    return Config()  # type: ignore[reportCallIssue]
