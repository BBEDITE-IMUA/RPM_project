from datetime import datetime
from typing import Any, Dict

from sqlalchemy.exc import IntegrityError

from consumer.logger import logger
from consumer.storage.db import async_session
from src.model.models import Languages, User


async def register_user(body: Dict[str, Any]) -> None:
    logger.info('Accepting a registration request', body)

    user_id = body.get('user_id')
    language_id = body.get('language_id')

    if not user_id or not language_id:
        logger.error('Invalid registration request. Missing user_id or language_id')
        return

    async with async_session() as db:
        language = await db.get(Languages, language_id)
        if not language:
            logger.error(f'Language with id {language_id} not found')
            return

        user = User(user_id=user_id, language_id=language_id, registration_date=datetime.utcnow())
        db.add(user)

        try:
            await db.commit()
            logger.info(f'User {user_id} registered successfully')
        except IntegrityError as e:
            logger.error(f'Error during user registration: {e}')
            await db.rollback()
