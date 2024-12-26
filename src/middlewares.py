import aio_pika
import msgpack
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n.middleware import I18nMiddleware

from config.settings import settings
from consumer.storage import rabbit
from src.templates.constants import AVALIABLE_LANGUAGES


class CustomI18nMiddleware(I18nMiddleware):
    async def get_supported_language(self, language: str):
        if language in AVALIABLE_LANGUAGES:
            return language
        return self.i18n.default_locale

    async def get_locale(self, event, data):
        state: FSMContext = data.get('state')
        state_data = await state.get_data()
        user_state_language = state_data.get('language')
        if user_state_language:
            return await self.get_supported_language(user_state_language)

        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
            user_language_from_db = await self.get_user_language_from_queue(user_id)

            if user_language_from_db:
                await state.update_data(language=user_language_from_db)
                return user_language_from_db

            user_device_language = await self.get_supported_language(event.from_user.language_code)
            await state.update_data(language=user_device_language)
            return user_device_language

        return self.i18n.default_locale

    async def get_user_language_from_queue(self, user_id: int) -> str:
        request_body = {'user_id': user_id, 'action': 'get_user_language'}

        async with rabbit.channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange('user_languages', aio_pika.ExchangeType.TOPIC, durable=True)

            response_queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=user_id), durable=True)

            user_queue = await channel.declare_queue('user_messages', durable=True)

            await response_queue.bind(exchange, routing_key=settings.USER_QUEUE.format(user_id=user_id))
            await user_queue.bind(exchange, routing_key='user_messages')

            await exchange.publish(aio_pika.Message(msgpack.packb(request_body)), routing_key='user_messages')

            async with response_queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        response = msgpack.unpackb(message.body)
                        return response.get('language', {}).get('locale')

        return None
