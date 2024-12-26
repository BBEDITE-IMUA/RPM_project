from typing import Any, Dict

import aio_pika
import msgpack
from aio_pika import ExchangeType
from sqlalchemy.future import select

from config.settings import settings
from consumer.logger import logger
from consumer.storage.db import async_session
from src.model.models import User
from src.storage.rabbit import channel_pool


async def check_user_in_db(body: Dict[str, Any]) -> None:
    user_id = body.get('user_id')

    if not user_id:
        logger.warning('Invalid request. Missing user_id')
        return

    async with async_session() as db:
        stmt = select(User).where(User.user_id == user_id)
        res = await db.execute(stmt)
        user = res.scalar_one_or_none()

        response_body = {
            'user_id': user_id,
            'exists': user is not None,
        }

    async with channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange('user_check', ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=user_id), durable=True)

        await queue.bind(exchange, routing_key=settings.USER_QUEUE.format(user_id=user_id))

        await exchange.publish(
            aio_pika.Message(msgpack.packb(response_body)),
            routing_key=settings.USER_QUEUE.format(user_id=user_id),
        )

        logger.info(f'Sent response for user_id={user_id}: {response_body}')
