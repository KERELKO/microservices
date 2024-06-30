import json
import pika

from src.exceptions import IncorrectCredentialsException
from src.config import config
from src.services import AuthService


async def handle_request(ch, method, properties: pika.BasicProperties, body: str | bytes) -> None:
    request = json.loads(body)
    print('auth_service: ', request)

    service = AuthService()
    try:
        token = await service.login(username=request['username'], password=request['password'])
    except IncorrectCredentialsException:
        token = IncorrectCredentialsException.__name__
    result = {'token': token}

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=json.dumps(result)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_service():
    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters(host=config.RMQ_HOST, port=config.RMQ_PORT),
    )
    channel = connection.channel()
    channel.queue_declare('auth_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='auth_queue', on_message_callback=handle_request)

    print(' [x] Awaiting authentication requests')
    channel.start_consuming()


if __name__ == '__main__':
    start_service()
