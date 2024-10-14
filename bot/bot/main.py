from bot.bot import *
import json
import logging
import traceback
import html


async def start(update: Update, context: CustomContext):
    if await is_group(update):
        return 

    if await is_registered(update.message.chat.id):
        # some functions
        await main_menu(update, context)
    else:
        hello_text = lang_dict['hello']
        await update.message.reply_text(
            hello_text,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[["UZ 🇺🇿", "RU 🇷🇺"]], resize_keyboard=True, one_time_keyboard=True
            ),
        )
        return SELECT_LANG


async def settings(update: Update, context: CustomContext):
    await make_button_settings(update, context)
    return ALL_SETTINGS

def search_drugs(update, context):
    return

async def about(update: Update, context: CustomContext):
    info = await get_info()
    user_lang = (await get_user_by_update(update)).lang
    if user_lang == 'uz' and info:
        text = info.about_uz
    elif user_lang == 'ru' and info:
        text = info.about_ru
    else:
        text = '🧾'

    await update_message_reply_text(update, text)
    

async def partners(update: Update, context: CustomContext):
    if info := await get_info():
        file = info.partners
        await bot_send_document(update, context, file)
    else:
        text = '🤝'
        await update_message_reply_text(update, text)
    await bot_send_message(update, context, get_word('our partners', update))

async def site(update: Update, context: CustomContext):
    text = (await get_info()).site if await get_info() else '🌐'
    await update_message_reply_text(update, text, disable_web_page_preview=False)


logger = logging.getLogger(__name__)

async def error_handler(update: Update, context: CustomContext):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=206261493, text=message, parse_mode=ParseMode.HTML
    )