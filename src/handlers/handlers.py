from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from src.templates import texts, keyboards
from crud import register_user
from db import AsyncSessionLocal
from bot_rabbitmq_sender import send_to_queue
from queue_name import USER_REGISTRATION


async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_language = message.from_user.language_code or 'en'

    await send_to_queue(USER_REGISTRATION, {'user_id': user_id, 'language': user_language})

    await message.answer(
        await texts.get_start_message(
            user = message.from_user.full_name
        ),
        reply_markup = await keyboards.get_start_keyboard()
    )


async def agreement_message(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        await texts.get_agreement_message(),
        reply_markup = await keyboards.get_agreement_keyboard()
    )


async def agree_with_terms(call: CallbackQuery, state: FSMContext):
    async with AsyncSessionLocal() as session:
        await register_user(session, call.from_user.id, call.from_user.language_code or 'en')
        await call.message.edit_text(
            await texts.get_agree_with_terms_message(),
            reply_markup = await keyboards.get_agree_with_terms_keyboard()
        )


async def disagree_with_terms(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        await texts.get_disagree_with_terms_message(),
        reply_markup = await keyboards.get_disagree_with_terms_keyboard()
    )


async def start_again(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        await texts.get_start_again_message(
            user = call.from_user.full_name
        ),
        reply_markup = await keyboards.get_start_keyboard()
    )


async def personal_account(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        await texts.get_personal_account_message(),
        reply_markup = await keyboards.get_personal_account_keyboard()
    )