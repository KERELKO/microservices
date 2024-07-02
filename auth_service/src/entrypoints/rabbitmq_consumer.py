from dataclasses import asdict
import asyncio
import functools
import json

import pika

from src.common.dto import UserReadDTO
from src.common.exceptions import IncorrectCredentialsException
from src.common.config import get_conf
from src.common.di import Container
from src.services.auth import AuthService


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return wrapper


@sync
async def handle_request(ch, method, properties: pika.BasicProperties, body: str | bytes) -> None:
    response = {
        'data': None,
        'meta': {'errors': None},
    }
    request = json.loads(body)
    service = Container.resolve(AuthService)
    token = request['token']
    try:
        u = await service.get_user_by_token(token)
    except IncorrectCredentialsException:
        response['meta']['errors'] = IncorrectCredentialsException.__name__
    else:
        user_data = asdict(UserReadDTO(id=u.id, username=u.username, email=u.email))
        response['data'] = user_data
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=json.dumps(response)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_service():
    conf = get_conf()
    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters(host=conf.RMQ_HOST, port=conf.RMQ_PORT),
    )
    channel = connection.channel()
    channel.queue_declare('auth_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='auth_queue', on_message_callback=handle_request)
    channel.start_consuming()


if __name__ == '__main__':
    start_service()
