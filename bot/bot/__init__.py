from bot import *
from telegram import Update, CallbackQuery, MenuButtonWebApp, WebAppInfo
from telegram.ext import ContextTypes, CallbackContext, ExtBot, Application
from dataclasses import dataclass
from asgiref.sync import sync_to_async
from bot.utils import *
from bot.utils.bot_functions import *
from bot.utils.keyboards import *
from bot.resources.strings import lang_dict
from bot.services import *
from bot.services.language_service import *
from bot.resources.conversationList import *

from app.services.drug_service import *
from app.services.info_service import *
from app.services.usage_service import *

from config import WEBAPP_URL


@dataclass
class WebhookUpdate:
    """Simple dataclass to wrap a custom update type"""
    user_id: int
    payload: str


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        if isinstance(update, WebhookUpdate):
            return cls(application=application, user_id=update.user_id)
        return super().from_update(update, application)


async def is_message_back(update: Update):
    if update.message.text == await get_word("back", update):
        return True
    else:
        return False


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update = update.callback_query if update.callback_query else update

    bot = context.bot
    keyboards = [
        # [get_word('search drugs', update)],
        [await get_word('about us', update), await get_word('our partners', update)],
        [await get_word('our site', update), await get_word('settings', update)],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard=keyboards, resize_keyboard=True)
    await bot.send_message(
        update.message.chat_id,
        await get_word('main menu', update),
        reply_markup=reply_markup
    )

    # set web app menu button
    web_app = WebAppInfo(f"{WEBAPP_URL}")
    menu_button = MenuButtonWebApp(
        text=await get_word("search drugs", update),
        web_app=web_app)
    await context.bot.set_chat_menu_button(context._user_id, menu_button=menu_button)

    await check_username(update)


async def make_button_settings(update: Update, context: CustomContext):
    await bot.send_message(
        update.effective_chat.id,
        await get_word("settings desc", update),
        reply_markup=ReplyKeyboardMarkup(keyboard=await settings_keyboard(update), resize_keyboard=True),
    )
