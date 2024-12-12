import aio_pika
import asyncio
import json
from db import AsyncSessionLocal
from crud import register_user
from config import settings
from queue_name import USER_REGISTRATION


async def listen_to_queue():
    connection = await aio_pika.connect(settings.RABBITMQ_HOST)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(USER_REGISTRATION)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode('utf-8'))

                    async with AsyncSessionLocal() as session:
                        await register_user(session, data['user_id'], data['language'])

if __name__ == "__main__":
    asyncio.run(listen_to_queue())