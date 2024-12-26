import logging.config

import msgpack

from consumer.handlers.event_distribution import handle_event_distribution
from consumer.logger import LOGGING_CONFIG, logger
from consumer.storage import rabbit
from consumer.metrics import RECEIVE_MESSAGE


async def main() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger.info('Starting consumer')
    async with rabbit.channel_pool.acquire() as channel:
        await channel.set_qos(
            prefetch_count=10,
        )

        queue = await channel.declare_queue('user_messages', durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    RECEIVE_MESSAGE.inc()
                    body = msgpack.unpackb(message.body)
                    await handle_event_distribution(body)
