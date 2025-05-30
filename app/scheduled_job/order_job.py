import asyncio
import os
import pandas as pd
from asgiref.sync import sync_to_async
from bot.control.updater import application
from app.models import Order, OrderItem, Provider
from bot.models import Bot_user

async def send_order_notifications():
    os.makedirs("files/order", exist_ok=True)
    async for order in Order.objects.filter(sent_to_provider=False):
        bot_user: Bot_user = await order.get_bot_user
        provider_items = {}
        async for item in OrderItem.objects.filter(order=order):
            provider = await Provider.objects.filter(
                name__contains=item.provider_name.lower()
                ).exclude(tg_id=None).afirst()
            if provider:
                if provider.tg_id not in provider_items:
                    provider_items[provider.tg_id] = []
                provider_items[provider.tg_id].append(item)
        
        for tg_id, items in provider_items.items():
            # Prepare data for Excel
            data = [
                ["Заказчик", bot_user.name],
                ["Username", bot_user.username],
                ["Телефон", bot_user.phone],
                [],
                ["№", "Название", "Производитель", "Страна", "Цена", "Количество"]
            ]
            for idx, item in enumerate(items, start=1):
                data.append([idx, item.title, item.manufacturer, item.country, item.price, item.count])
            
            # Save Excel file
            df = pd.DataFrame(data)
            file_path = f"files/order/order_{order.id}.xlsx"
            df.to_excel(file_path, index=False, header=False)

            # Prepare text message
            message = (
                f"Заказчик: {bot_user.name}\n"
                f"Username: @{bot_user.username}\n"
                f"Телефон: {bot_user.phone}\n\n"
                "Детали заказа:\n"
            )
            for idx, item in enumerate(items, start=1):
                message += (
                    f"{idx}. {item.title}\n"
                    f"   Производитель: {item.manufacturer}\n"
                    f"   Страна: {item.country}\n"
                    f"   Цена: {item.price}\n"
                    f"   Количество: {item.count}\n\n"
                )

            # Send text message and Excel file
            try:
                await application.bot.send_message(chat_id=tg_id, text=message)
                await application.bot.send_document(chat_id=tg_id, document=open(file_path, 'rb'))
            except:
                pass
        order.sent_to_provider = True
        await order.asave()
