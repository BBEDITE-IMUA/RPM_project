from aiogram.utils.i18n.middleware import I18nMiddleware
from aiogram.fsm.context import FSMContext
from db import AsyncSessionLocal
from crud import get_user_language
from VpnKeySellerBot.src.templates.constants import AVALIABLE_LANGUAGES
from aiogram.types import Message

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
            return await self.get_supported_language(
                user_state_language
            )

        if isinstance(event, Message) and event.from_user:
            async with AsyncSessionLocal() as session:
                user_language_from_db = await get_user_language(session, str(event.from_user.id))
                if user_language_from_db:
                    await state.update_data(language=user_language_from_db)
                    return user_language_from_db

                user_device_language = await self.get_supported_language(
                    event.from_user.language_code
                )
                await state.update_data(language=user_device_language)
                return user_device_language

        return self.i18n.default_locale
