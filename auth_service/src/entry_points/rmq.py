import json
import pika

from src.config import config


def handle_rmq_request(ch, method, properties: pika.BasicProperties, body: str | bytes) -> None:
    request = json.loads(body)

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=json.dumps(body)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_service():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.RMQ_HOST, port=config.RMQ_PORT),
    )
    channel = connection.channel()
    channel.queue_declare('auth_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='auth_queue', on_message_callback=handle_rmq_request)

    print(' [x] Awaiting authentication requests')
    channel.start_consuming()
