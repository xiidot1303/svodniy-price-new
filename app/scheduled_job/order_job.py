from asgiref.sync import sync_to_async
from bot.control.updater import application
from app.models import Order, OrderItem, Provider
from bot.models import Bot_user

async def send_order_notifications():
    async for order in Order.objects.filter(sent_to_provider=False):
        bot_user: Bot_user = await order.get_bot_user
        provider_items = {}
        async for item in OrderItem.objects.filter(order=order):
            provider = await Provider.objects.filter(name__contains=item.provider_name.lower()).afirst()
            if provider:
                if provider.tg_id not in provider_items:
                    provider_items[provider.tg_id] = []
                provider_items[provider.tg_id].append(item)
        
        for tg_id, items in provider_items.items():
            message = (
                f"Новые заказы от {bot_user.name} @{bot_user.username}\n"
                f"Телефон: {bot_user.phone}\n\n"
                "Детали заказа:\n"
            )
            for item in items:
                message += f"<b>{item.title}</b> x {item.count}\n"
            await application.bot.send_message(chat_id=tg_id, text=message, parse_mode='HTML')
        order.sent_to_provider = True
        await order.asave()
