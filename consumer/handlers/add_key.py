from datetime import datetime
from typing import Any, Dict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from consumer.logger import logger
from consumer.storage.db import async_session
from src.model.models import Countries, Keys, User


async def add_key_for_user(body: Dict[str, Any]) -> None:
    user_id = body.get('user_id')
    country_id = body.get('country_id')
    encrypted_key = body.get('encrypted_key')
    expires_at = body.get('expires_at')

    if not user_id or not country_id or not encrypted_key or not expires_at:
        logger.error('Invalid request. Missing user_id, country_id, encrypted_key, or expires_at')
        return

    async with async_session() as db:
        user = await db.execute(select(User).where(User.user_id == user_id))
        user = user.scalars().first()

        country = await db.execute(select(Countries).where(Countries.id == country_id))
        country = country.scalars().first()

        if not user:
            logger.error(f'User with id {user_id} not found')
            return

        if not country:
            logger.error(f'Country with id {country_id} not found')
            return

        new_key = Keys(
            user_id=user_id,
            country_id=country_id,
            encrypted_key=encrypted_key,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
        )
        db.add(new_key)

        try:
            await db.commit()
            logger.info(f'Key for user {user_id} added successfully')
        except IntegrityError as e:
            logger.error(f'Error during key addition for user {user_id}: {e}')
            await db.rollback()
