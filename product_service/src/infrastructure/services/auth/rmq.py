import asyncio
import uuid

import aio_pika as apika
import orjson

from src.common.config import get_conf
from src.infrastructure.dto.auth import User

from .base import AbstractAuthService, AuthServiceException


class RabbitAuthService(AbstractAuthService[User]):
    def __init__(self, conn_string: str | None = None) -> None:
        self.corr_id: str | None = None
        self.conn_string = conn_string or get_conf().rabbitmq_connection_string

    async def on_response(self, message: apika.IncomingMessage) -> None:
        if self.corr_id == message.correlation_id:
            self.response = orjson.loads(message.body)
            await message.ack()

    async def get_user_by_token(self, token: str) -> User:
        self.corr_id = str(uuid.uuid4())
        self.response = None

        connection = await apika.connect_robust(url=self.conn_string, timeout=10)
        channel = await connection.channel()
        self.callback_queue = await channel.declare_queue('', exclusive=True)
        await self.callback_queue.consume(self.on_response)  # type: ignore
        await channel.default_exchange.publish(
            apika.Message(
                body=orjson.dumps({'token': token}),
                correlation_id=self.corr_id,
                reply_to=self.callback_queue.name
            ),
            routing_key='auth_queue'
        )

        while self.response is None:
            await asyncio.sleep(0.02)

        if self.response['data'] is not None and not self.response['errors']:
            data = self.response['data']
            user = User(**data)
            return user
        raise AuthServiceException('Failed to process the response', self.response)
