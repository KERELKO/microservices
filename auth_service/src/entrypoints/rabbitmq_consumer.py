from dataclasses import asdict

import orjson

import aio_pika as apika
from pamqp import commands as spec

import uvloop

from src.common.utils import raise_exc
from src.common.dto import UserReadDTO
from src.common.exceptions import DomainException
from src.common.config import get_conf
from src.common.di import Container
from src.services.auth import AuthService


async def handle_request(message: apika.abc.AbstractIncomingMessage) -> None:
    response = {
        'data': None,
        'meta': {},
        'errors': [],
    }
    request = orjson.loads(message.body)
    service: AuthService = Container.resolve(AuthService)

    try:
        token = t if (t := request.get('token', None)) else raise_exc(DomainException('No token'))
        u: UserReadDTO = await service.get_user_by_token(token)
    except DomainException as e:
        response['errors'].append(e.__repr__())
    else:
        user_data = asdict(UserReadDTO(id=u.id, username=u.username, email=u.email))
        response['data'] = user_data

    await message.channel.basic_publish(
        exchange='',
        routing_key=message.reply_to,  # type: ignore[reportArgumentType]
        properties=spec.Basic.Properties(correlation_id=message.properties.correlation_id),
        body=orjson.dumps(response)
    )

    await message.channel.basic_ack(
        delivery_tag=message.delivery_tag  # type: ignore[reportArgumentType]
    )


async def start_service() -> None:
    conf = get_conf()
    connection = await apika.connect_robust(
        host=conf.RABBITMQ_HOST, port=conf.RABBITMQ_PORT, timeout=25,
    )

    async with connection:
        queue_name = 'auth_queue'

        channel: apika.abc.AbstractChannel = await connection.channel()

        queue: apika.abc.AbstractQueue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await handle_request(message)


def main() -> None:
    uvloop.run(start_service())


if __name__ == '__main__':
    main()
