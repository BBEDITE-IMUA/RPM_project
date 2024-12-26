from typing import Any, Dict

import aio_pika
import msgpack
from sqlalchemy.future import select

from config.settings import settings
from consumer.logger import logger
from consumer.storage import rabbit
from consumer.storage.db import async_session
from src.model.models import Keys


async def get_keys_for_user(body: Dict[str, Any]) -> None:
    logger.info('Get keys for user', body)

    user_id = body.get('user_id')
    if not user_id:
        logger.error('Invalid request. Missing user_id')
        return

    async with async_session() as db:
        result = await db.execute(select(Keys).where(Keys.user_id == user_id))
        keys = result.scalars().all()

        response_body = {
            'user_id': user_id,
            'keys': [key.to_dict() for key in keys],
        }

    async with rabbit.channel_pool.acquire() as channel:

        exchange = await channel.declare_exchange('user_keys', aio_pika.ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=user_id), durable=True)

        await queue.bind(exchange, routing_key=settings.USER_QUEUE.format(user_id=user_id))

        await exchange.publish(
            aio_pika.Message(msgpack.packb(response_body)),
            routing_key=settings.USER_QUEUE.format(user_id=user_id),
        )
        logger.info(f'Sent keys for user {user_id}: {response_body}')
