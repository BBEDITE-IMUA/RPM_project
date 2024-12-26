import aio_pika
import msgpack
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config.settings import settings
from src.storage import rabbit
from src.templates import keyboards, texts
from src.metrics import track_latency, SEND_MESSAGE


@track_latency('start')
async def start(message: Message, state: FSMContext) -> None:
    if not message.from_user:
        await message.answer('Не удалось получить данные пользователя.')
        return

    user_id = message.from_user.id
    request_body = {'user_id': user_id, 'action': 'check_user_in_db'}

    async with rabbit.channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange('user_check', aio_pika.ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=user_id), durable=True)

        user_queue = await channel.declare_queue('user_messages', durable=True)

        await user_queue.bind(exchange, 'user_messages')

        await queue.bind(exchange, routing_key=settings.USER_QUEUE.format(user_id=user_id))

        await exchange.publish(
            aio_pika.Message(
                body=msgpack.packb(request_body)
            ),
            routing_key='user_messages'
        )

        SEND_MESSAGE.inc()

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    response = msgpack.unpackb(message.body)
                    break

    if response.get('exists'):
        await message.answer(
            await texts.get_start_again_message(user=message.from_user.full_name),
            reply_markup=await keyboards.get_agree_with_terms_keyboard()
        )
    else:
        await message.answer(
            await texts.get_start_message(user=message.from_user.full_name),
            reply_markup=await keyboards.get_start_keyboard()
        )


@track_latency('agreement_message')
async def agreement_message(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(
        await texts.get_agreement_message(),
        reply_markup = await keyboards.get_agreement_keyboard()
    )


@track_latency('agree_with_terms')
async def agree_with_terms(call: CallbackQuery, state: FSMContext) -> None:
    if call.from_user is None:
        await call.message.answer('Не удалось получить данные о пользователе')
        return
    
    async with rabbit.channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange('user_actions', aio_pika.ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=call.from_user.id), durable=True)

        user_queue = await channel.declare_queue('user_messages', durable=True)

        
        await queue.bind(exchange, routing_key=settings.USER_QUEUE.format(user_id=call.from_user.id))
        await user_queue.bind(exchange, routing_key='user_messages')

        body = {'user_id': call.from_user.id, 'action': 'register_user'}

        await channel.default_exchange.publish(
            aio_pika.Message(msgpack.packb(body)),
            routing_key='user_messages',
        )

        SEND_MESSAGE.inc()

    await call.message.edit_text(
        await texts.get_agree_with_terms_message(),
        reply_markup = await keyboards.get_agree_with_terms_keyboard()
    )


@track_latency('disagree_with_terms')
async def disagree_with_terms(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(
        await texts.get_disagree_with_terms_message(),
        reply_markup = await keyboards.get_disagree_with_terms_keyboard()
    )


@track_latency('start_again')
async def start_again(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(
        await texts.get_start_again_message(
            user = call.from_user.full_name
        ),
        reply_markup = await keyboards.get_start_keyboard()
    )


@track_latency('personal_account')
async def personal_account(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(
        await texts.get_personal_account_message(),
        reply_markup = await keyboards.get_personal_account_keyboard()
    )


@track_latency('my_subscription')
async def my_subscription(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(
        await texts.get_my_subscription_message(),
        reply_markup = await keyboards.get_personal_account_keyboard()
    )


@track_latency('change_language')
async def change_language(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(
        await texts.change_language_message(),
        reply_markup = await keyboards.change_language_keyboard()
    )


@track_latency('choose_ru_language')
async def choose_ru_language(call: CallbackQuery, state: FSMContext) -> None:
    await update_language(call, 1, state)


@track_latency('choose_en_language')
async def choose_en_language(call: CallbackQuery, state: FSMContext) -> None:
    await update_language(call, 2, state)
    

async def update_language(call: CallbackQuery, language_id: int, state: FSMContext) -> None:
    user_id = call.from_user.id

    response_body = {
        'user_id': user_id,
        'language_id': language_id,
        'action': 'update_user_language',
    }

    async with rabbit.channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange('user_languages', aio_pika.ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=user_id), durable=True)

        user_queue = await channel.declare_queue('user_messages', durable=True)

        await queue.bind(exchange, routing_key=settings.USER_QUEUE.format(user_id=user_id))
        await user_queue.bind(exchange, routing_key='user_messages')

        await channel.default_exchange.publish(
            aio_pika.Message(msgpack.packb(response_body)),
            routing_key='user_messages',
        )

        SEND_MESSAGE.inc()


@track_latency('by_subscription')
async def by_subscription(call: CallbackQuery, state: FSMContext) -> None:
    return None
