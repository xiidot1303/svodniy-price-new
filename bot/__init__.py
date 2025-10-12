from dataclasses import dataclass
from typing import Optional
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ContextTypes,
    ExtBot,
    TypeHandler,
    PicklePersistence
)
from telegram import (
    ReplyKeyboardMarkup
)



@dataclass
class NewsletterUpdate:
    user_id: int
    text: str = None
    photo: Optional[object | str] = None
    video: Optional[object | str] = None
    document: Optional[object] = None
    reply_markup: Optional[ReplyKeyboardMarkup] = None
    pin_message: bool = False