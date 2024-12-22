from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from src.api.router import router
from src.bot import bot, dp
from src.logger import logger, set_correlation_id


@router.post('/home')
async def home(request: Request) -> ORJSONResponse:
    correlation_id = set_correlation_id()
    logger.info(f'Getting a request from telegram, Correlation ID: {correlation_id}')
    update = await request.json()

    await dp.feed_webhook_update(bot, update)
    logger.info(f'Request processed, Correlation ID: {correlation_id}')
    return ORJSONResponse({'status': 'ok'})
