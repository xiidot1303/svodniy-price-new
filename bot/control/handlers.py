from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler,
    TypeHandler,
    ConversationHandler
)

from bot.resources.strings import lang_dict
from bot.resources.conversationList import *

from bot.bot import (
    main,
)

exceptions_for_filter_text = (~filters.COMMAND) & (~filters.Text(lang_dict['main menu']))

start = CommandHandler('start', main.start)

handlers = [
    start
]