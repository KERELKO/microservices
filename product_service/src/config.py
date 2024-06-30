from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    MONGO_DB_HOST: str
    MONGO_DB_PORT: str

    RMQ_HOST: str = Field(default='rabbitmq')
    RMQ_PORT: int = Field(default=5672)

    @property
    def mongo_db_uri(self) -> str:
        return f'mongodb://{self.MONGO_DB_HOST}:{self.MONGO_DB_PORT}/'

    def get_async_mongo_client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(host=self.MONGO_DB_HOST, port=int(self.MONGO_DB_PORT))


config = Config()  # type: ignore
