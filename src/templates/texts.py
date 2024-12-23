from aiogram.utils.i18n import gettext as _
import msgpack
import aio_pika
from config.settings import settings
from consumer.storage import rabbit

async def get_start_message(user: str):
    return _(
        "👋 <b>Hello, {user}!</b>\n\n"
        "Here you can buy a <b>VPN</b> subscription 🛡️\n"
        "Tap the button below this message to continue ⬇️"
    ).format(user=user)

async def get_agreement_message():
    return _(
        "📜 <b>Before we begin we need to make some agreements 📜</b>\n\n"
        "After reading, click <b>\"✅ I agree\"</b> to continue.\n\n"
    )

async def get_agree_with_terms_message() -> str:
    # спасибо, что согласились с условиями, вы успешно зарегистрированы, нажмите кнопку ниже, чтобы перейти в личный кабинет
    return _(
        "You've successfully registered! 🎉\n"
        "Click the button below to go to your personal account ⬇️"
    )

async def get_disagree_with_terms_message() -> str:
    # "🚫 <b>Вы отказались от условий.</b>\n\n"
    #     "😔 Сожалеем, но мы не можем предоставить вам услугу, пока вы не примите условия.\n\n"
    return _(
        "🚫 <b>You have declined the terms.</b>\n\n"
        "😔 We're sorry, but we can't provide you the service until you accept the terms.\n\n"
    )




async def get_start_again_message(user: str):
    # f"🎉 <b>Рады видеть тебя снова, {user}!</b>\n\n"
    #     "Здесь ты сможешь купить <b>VPN</b> подписку 🛡️\n\n"
    #     "Нажми на кнопку ниже, чтобы начать ⬇️"
    return _(
        "🎉 <b>Welcome back, {user}!</b>\n\n"
        "Here you can buy a <b>VPN</b> subscription 🛡️\n"
        "Tap the button below this message to continue ⬇️"
    ).format(user=user)


async def get_personal_account_message():
    # "👤 <b>Личный кабинет</b>\n\n"
    #     "Здесь ты мож
    return _(
        "📜<b> Choose an action</b>"
    )

async def change_language_message():
    return _(
        "🌍 <b>Choose language</b>"
    )

async def get_my_subscription_message(user_id: int) -> str:
    request_body = {
        'user_id': user_id,
        'action': 'get_keys_for_user',
    }
    
    async with rabbit.channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange('user_keys', aio_pika.ExchangeType.TOPIC, durable=True)

        user_queue = await channel.declare_queue('user_messages', durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=user_id), durable=True)

        await queue.bind(exchange, routing_key=settings.USER_QUEUE.format(user_id=user_id))
        await user_queue.bind(exchange, 'user_messages')

        await exchange.publish(
            aio_pika.Message(
                body=msgpack.packb(request_body),
            ),
            routing_key='user_messages'
        )

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    response = msgpack.unpackb(message.body)
                    break

    keys = response.get('keys', [])
    if not keys:
        return _(
            "👤 <b>Personal account</b>\n\n"
            "You don't have any active subscriptions 📦\n"
        )

    keys_text = "\n".join(
        _(
            "Key: <code>{key}</code>, Status: <b>{status}</b>, Expiry Date: {expiry_date}"
        ).format(
            key=key['value'],
            status=key['status'],
            expiry_date=key['expiry_date'],
        )
        for key in keys
    )
    return _(
        "👤 <b>Personal account</b>\n\n"
        "Here you can manage your subscription 📦\n\n"
        "Your active subscriptions:\n{keys_text}"
    ).format(keys_text=keys_text)
    

async def buy_vpn_message():
    return _(
        "📜<b> Choose an action</b>"
    )
