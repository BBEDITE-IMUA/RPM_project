from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
import handlers
import constants

user_router = Router()

user_router.message.register(handlers.start, CommandStart())
user_router.callback_query.register(handlers.agreement_message, F.data == constants.CONTINUE_INLINE_BUTTON_CALL)
user_router.callback_query.register(handlers.agree_with_terms, F.data == constants.AGREE_INLINE_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.disagree_with_terms, F.data == constants.DISAGREE_INLINE_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.start_again, F.data == constants.LETS_START_AGAING_INLINE_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.personal_account, F.data == constants.PERSONAL_ACCOUNT_INLINE_BUTTON_CALLBACK)