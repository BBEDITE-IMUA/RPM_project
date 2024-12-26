from typing import Any, Dict

from consumer.handlers.add_key import add_key_for_user
from consumer.handlers.check_user_in_db import check_user_in_db
from consumer.handlers.get_user_keys import get_keys_for_user
from consumer.handlers.get_user_language import get_user_language
from consumer.handlers.login import register_user
from consumer.handlers.update_user_language import update_user_language


async def handle_event_distribution(body: Dict[str, Any]) -> None:
    match body['action']:
        case 'register_user':
            await register_user(body)
        case 'check_user_in_db':
            await check_user_in_db(body)
        case 'update_user_language':
            await update_user_language(body)
        case 'get_user_language':
            await get_user_language(body)
        case 'add_key_for_user':
            await add_key_for_user(body)
        case 'get_keys_for_user':
            await get_keys_for_user(body)
