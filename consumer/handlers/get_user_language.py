import aio_pika
import msgpack
from sqlalchemy.future import select
from typing import Dict, Any
from src.model.models import User, Languages
from config.settings import settings
from consumer.storage import rabbit
from consumer.logger import logger
from consumer.storage.db import async_session


async def get_user_language(body: Dict[str, Any]) -> None:
    user_id = body.get('user_id')
    if not user_id:
        logger.error('Invalid request. Missing user_id')
        return

    async with async_session() as db:
        result = await db.execute(select(User).where(User.user_id == user_id))
        user = result.scalars().first()

        if not user:
            logger.error(f'User with id {user_id} not found')
            return

        language = await db.execute(select(Languages).where(Languages.id == user.language_id))
        language = language.scalars().first()

        if not language:
            logger.error(f'Language with id {user.language_id} not found')
            return

        response_body = {
            'user_id': user_id,
            'language': {
                'name': language.name,
                'locale': language.locale,
            }
        }

    async with rabbit.channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange('user_languages', aio_pika.ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=user_id), durable=True)

        await queue.bind(exchange, routing_key=settings.USER_QUEUE.format(user_id=user_id))

        await exchange.publish(
            aio_pika.Message(msgpack.packb(response_body)),
            routing_key=settings.USER_QUEUE.format(user_id=user_id),
        )

        logger.info(f'Sent language for user {user_id}: {response_body}')
