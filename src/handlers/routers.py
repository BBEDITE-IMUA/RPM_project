from aiogram import Router, F
from aiogram.filters import CommandStart
import VpnKeySellerBot.src.handlers.handlers as handlers
import VpnKeySellerBot.src.templates.constants as constants

user_router = Router()

user_router.message.register(handlers.start, CommandStart())
user_router.callback_query.register(handlers.agreement_message, F.data == constants.CONTINUE_INLINE_BUTTON_CALL)
user_router.callback_query.register(handlers.agree_with_terms, F.data == constants.AGREE_INLINE_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.disagree_with_terms, F.data == constants.DISAGREE_INLINE_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.start_again, F.data == constants.LETS_START_AGAING_INLINE_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.personal_account, F.data == constants.PERSONAL_ACCOUNT_INLINE_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.by_subscription, F.data == constants.BY_SUBSCRIPTION_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.change_language, F.data == constants.CHENGE_LANGUAGE_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.my_subscription, F.data == constants.MY_SUBSCRIPTION_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.choose_ru_language, F.data == constants.RUSSIAN_LANGUAGE_BUTTON_CALLBACK)
user_router.callback_query.register(handlers.choose_en_language, F.data == constants.ENGLISH_LANGUAGE_BUTTON_CALLBACK)
