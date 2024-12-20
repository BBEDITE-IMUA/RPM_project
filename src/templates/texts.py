from aiogram.utils.i18n import gettext as _

async def get_start_message(user: str):
    return _(
        "👋 <b>Hello, {user}!</b>\n\n"
        "Here you can buy a <b>VPN</b> subscription 🛡️\n"
        "Tap the button below this message to continue ⬇️"
    ).format(user=user)

async def get_agreement_message():
    return _(
        "📜 <b>Before we begin we need to make some agreements 📜</b>\n\n"
        "After reading, click <b>\"✅ I agree\"</b> to continue.\n\n"
    )

async def get_agree_with_terms_message() -> str:
    # спасибо, что согласились с условиями, вы успешно зарегистрированы, нажмите кнопку ниже, чтобы перейти в личный кабинет
    return _(
        "You've successfully registered! 🎉\n"
        "Click the button below to go to your personal account ⬇️"
    )

async def get_disagree_with_terms_message() -> str:
    # "🚫 <b>Вы отказались от условий.</b>\n\n"
    #     "😔 Сожалеем, но мы не можем предоставить вам услугу, пока вы не примите условия.\n\n"
    return _(
        "🚫 <b>You have declined the terms.</b>\n\n"
        "😔 We're sorry, but we can't provide you the service until you accept the terms.\n\n"
    )




async def get_start_again_message(user: str):
    # f"🎉 <b>Рады видеть тебя снова, {user}!</b>\n\n"
    #     "Здесь ты сможешь купить <b>VPN</b> подписку 🛡️\n\n"
    #     "Нажми на кнопку ниже, чтобы начать ⬇️"
    return _(
        "🎉 <b>Welcome back, {user}!</b>\n\n"
        "Here you can buy a <b>VPN</b> subscription 🛡️\n"
        "Tap the button below this message to continue ⬇️"
    ).format(user=user)

async def get_personal_account_message():
    # "👤 <b>Личный кабинет</b>\n\n"
    #     "Здесь ты мож
    return _(
        "👤 <b>Personal account</b>\n\n"
        "Here you can manage your subscription 📦\n"
    )