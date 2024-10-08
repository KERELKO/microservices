import asyncio
from uuid import uuid4

import grpc.experimental
import grpc
import grpc_.unary_auth_pb2_grpc as pb2_grpc
import grpc_.unary_auth_pb2 as pb2

import aio_pika as apika
import uuid
import orjson

from src.services.exceptions import AuthServiceException
from src.repositories.base import AbstractRepository
from src.common.dto import Product, User
from src.common.config import get_conf

from .base import AbstractAuthService, AbstractProductService


class ProductService(AbstractProductService[Product]):
    def __init__(self, repository: AbstractRepository) -> None:
        self.repo = repository

    async def get_list(self, offset: int = 0, limit: int = 20) -> list[Product]:
        products = await self.repo.get_list(offset=offset, limit=limit)
        return products

    async def create(self, product: Product) -> None:
        await self.repo.create(product)

    async def get_by_id(self, id: str) -> Product | None:
        product = await self.repo.get(id=id)
        return product


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


class gRPCAuthService(AbstractAuthService[User]):
    def __init__(self, url: str | None = None) -> None:
        self.conf = get_conf()
        self.url = url or self.conf.grpc_uri

    async def get_user_by_token(self, token: str) -> User:
        async with grpc.aio.insecure_channel(self.url) as channel:
            stub = pb2_grpc.AuthServiceStub(channel)
            response: pb2.Response = await stub.GetUserByToken(pb2.RequestUser(token=token))
            data = response.data

        if not response.errors and data:
            _user: pb2.User = data
            user = User(id=str(_user.id), username=_user.username, email=_user.email)
            return user

        raise AuthServiceException('Failed to process the response', response.errors, self.url)


class FakeAuthService(AbstractAuthService[User]):
    async def get_user_by_token(self, token: str) -> User:
        return User(id=f'{uuid4()}', username=f'test-user-token:{token}', email='test@user.com')
