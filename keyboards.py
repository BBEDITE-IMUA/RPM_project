from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import constants

async def get_start_keyboard() -> InlineKeyboardMarkup:
    Keyboard = [
        [
            InlineKeyboardButton(text = str(constants.CONTINUE_INLINE_BUTTON_TEXT), callback_data=constants.CONTINUE_INLINE_BUTTON_CALL)
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard = Keyboard
    )


async def get_agreement_keyboard() -> InlineKeyboardMarkup:
    Keyboard = [
        [
            InlineKeyboardButton(text = str(constants.TERMS_INLINE_BUTTON_TEXT), url = constants.TERMS_INLINE_BUTTON_URL),
            InlineKeyboardButton(text = str(constants.AGREE_INLINE_BUTTON_TEXT), callback_data = constants.AGREE_INLINE_BUTTON_CALLBACK),
            InlineKeyboardButton(text = str(constants.DISAGREE_INLINE_BUTTON_TEXT), callback_data = constants.DISAGREE_INLINE_BUTTON_CALLBACK)
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard = Keyboard
    )


async def get_agree_with_terms_keyboard() -> InlineKeyboardMarkup:
    Keyboard = [
        [
            InlineKeyboardButton(text = str(constants.PERSONAL_ACCOUNT_INLINE_BUTTON_TEXT), callback_data = constants.PERSONAL_ACCOUNT_INLINE_BUTTON_CALLBACK)
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=Keyboard
    )


async def get_disagree_with_terms_keyboard() -> InlineKeyboardMarkup:
    Keyboard = [
        [
            InlineKeyboardButton(text = str(constants.LETS_START_AGAING_INLINE_BUTTON_TEXT), callback_data = constants.LETS_START_AGAING_INLINE_BUTTON_CALLBACK)
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard = Keyboard
    )


async def get_personal_account_keyboard() -> InlineKeyboardMarkup:
    Keyboard = [
        [
            InlineKeyboardButton(text = str(constants.MY_SUBSCRIPTION_BUTTON_TEXT), callback_data = constants.MY_SUBSCRIPTION_BUTTON_CALLBACK),
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard = Keyboard
    )
