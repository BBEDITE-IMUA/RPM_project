import asyncio
import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

from config.settings import settings
from src.api.router import router
from src.bot import bot, dp
from src.log_config import LOGGING_CONFIG, logging
from src.logger import set_correlation_id
from src.middlewares import CustomI18nMiddleware

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '...'))

logger = logging.getLogger('backend_logger')


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logging.config.dictConfig(LOGGING_CONFIG)

    polling_task: asyncio.Task[None] | None = None

    webhook_info = await bot.get_webhook_info()

    if settings.BOT_WEBHOOK_URL and webhook_info.url != settings.BOT_WEBHOOK_URL:
        await bot.set_webhook(settings.BOT_WEBHOOK_URL)
    else:
        polling_task = asyncio.create_task(dp.start_polling(bot, handle_signals=False))

    yield

    if polling_task is not None:
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            logger.info('Polling task was cancelled')

    await bot.delete_webhook()


def create_app() -> FastAPI:
    correlation_id = set_correlation_id()
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.include_router(router)
    app.add_middleware(CustomI18nMiddleware)
    logger.info(f'Application started, Correlation ID: {correlation_id}')
    return app


if __name__ == '__main__':
    uvicorn.run('src.app:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)
