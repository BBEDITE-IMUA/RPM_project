import aio_pika
from aio_pika import Channel
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from config.settings import settings


async def get_connection() -> AbstractRobustConnection:
    connection = await aio_pika.connect_robust(settings.rebbitmq_url)
    return connection


connection_pool: Pool = Pool(get_connection, max_size=5)


async def get_channel() -> Channel:
    async with connection_pool.acquire() as connection:
        return await connection.channel()


channel_pool: Pool = Pool(get_channel, max_size=10)
