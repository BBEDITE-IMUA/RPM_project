import asyncio
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares import CustomI18nMiddleware
from config import settings
import constants
from routers import user_router
from db import init_db

i18n = I18n(path=constants.LOCALES_PATH)

async def main():

    await init_db()

    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)


    CustomI18nMiddleware(i18n).setup(dp)

    dp.include_router(user_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
