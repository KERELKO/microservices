import json
from typing import Any

import pika
import uuid

from src.repositories.base import AbstractRepository
from src.repositories.mongo import ProductMongoRepository
from src.models import Product
from src.config import config

from .base import AbstractService


class ProductService(AbstractService[Product]):
    def __init__(self, repository: AbstractRepository | None = None) -> None:
        self.repo = ProductMongoRepository()

    async def get_list(self, offset: int = 0, limit: int = 20) -> list[Product]:
        products = await self.repo.get_list(offset=offset, limit=limit)
        return products

    async def create(self, product: Product) -> None:
        await self.repo.create(product)

    async def get_by_id(self, id: str) -> Product | None:
        product = await self.repo.get(id=id)
        return product


class RPCAuthClient:
    def __init__(self, host: str = config.RMQ_HOST, port: int = config.RMQ_PORT) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )
        self.corr_id: str | None = None

    def on_response(self, ch, method, props: pika.BasicProperties, body: str | bytes) -> None:
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, data: dict[str, Any]) -> dict[str, Any]:
        self.response: None | dict[str, Any] = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='auth_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(data)
        )
        while self.response is None:
            self.connection.process_data_events(time_limit=3)
        return self.response
