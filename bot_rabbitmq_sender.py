import aio_pika
import json
from config import settings

async def send_to_queue(queue_name, data):
    connection = await aio_pika.connect(settings.RABBITMQ_HOST)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(data).encode('utf-8')),
            routing_key=queue_name
        )
