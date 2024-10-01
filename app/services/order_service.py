from app.services import *
from bot.models import Bot_user
from app.models import Order, OrderItem

async def check_count_of_orders_of_bot_user(bot_user: Bot_user):
    count = await Order.objects.filter(bot_user__id = bot_user.id).acount()
    return count