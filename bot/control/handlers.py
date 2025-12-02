from bot import *
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
    main, login, orders
)

exceptions_for_filter_text = (~filters.COMMAND) & (~filters.Text(lang_dict['main menu']))

# HANDLERS

login_handler = ConversationHandler(
    entry_points=[CommandHandler("start", main.start)],
    states={
        SELECT_LANG: [MessageHandler(
            filters.Text(lang_dict["uz_ru"]) & exceptions_for_filter_text,
            login.select_lang
            )],
        GET_NAME: [MessageHandler(filters.TEXT & exceptions_for_filter_text, login.get_name)],
        GET_CONTACT: [MessageHandler(filters.ALL & exceptions_for_filter_text, login.get_contact)],
    },
    fallbacks=[
        CommandHandler('start', login.start)
    ],
    name="login",
    persistent=True,

)

orders_handler = MessageHandler(filters.Text(lang_dict['orders history']), main.orders_list)
load_more_orders_handler = CallbackQueryHandler(orders.send_orders_list, pattern = "load_more_orders")

about_handler = MessageHandler(filters.Text(lang_dict['about us']), main.about)
partners_handler = MessageHandler(filters.Text(lang_dict['our partners']), main.partners)
site_handler = MessageHandler(filters.Text(lang_dict['our site']), main.site)
settings_handler = MessageHandler(filters.Text(lang_dict["settings"]), main.settings)

handlers = [
    login_handler,
    about_handler,
    partners_handler,
    site_handler,
    settings_handler,
    orders_handler,
    load_more_orders_handler,
    TypeHandler(type=NewsletterUpdate, callback=main.newsletter_update)

]