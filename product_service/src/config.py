from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    MONGO_DB_HOST: str
    MONGO_DB_PORT: str

    @property
    def mongo_db_uri(self) -> str:
        return f'mongodb://{self.MONGO_DB_HOST}:{self.MONGO_DB_PORT}'

    def get_async_mongo_client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(self.MONGO_DB_HOST, self.MONGO_DB_PORT)


config = Config()  # type: ignore
