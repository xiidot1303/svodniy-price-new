from app.services import *
from bot.models import Bot_user
from app.models import Order, OrderItem
from bot.control.updater import application
from bot import NewsletterUpdate
import asyncio
import os
import pandas as pd
from asgiref.sync import sync_to_async
from bot.control.updater import application
from app.models import Order, OrderItem, Provider
from bot.models import Bot_user
import asyncio

async def check_count_of_orders_of_bot_user(bot_user: Bot_user):
    count = await Order.objects.filter(bot_user__id = bot_user.id).acount()
    return count


async def send_order_newsletter(order_id: int):
    await asyncio.sleep(2)
    order = await Order.objects.aget(id=order_id)
    operator = await order.get_operator
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
            "Общая сумма: <i>{total_price}</i> сум"
            "Детали заказа:\n"
        )
        total_price = 0
        for idx, item in enumerate(items, start=1):
            total_price += float(item.price)
            message += (
                f"{idx}. {item.title}\n"
                f"   Производитель: {item.manufacturer}\n"
                f"   Страна: {item.country}\n"
                f"   Цена: {item.price}\n"
                f"   Количество: {item.count}\n\n"
            )
        message.format(total_price = str(total_price))
        # Send text message and Excel file
        try:
            user_tg_id = operator.tg_id if operator else tg_id
            await application.update_queue.put(
                NewsletterUpdate(user_id=user_tg_id, text=message)
                )
            await application.update_queue.put(
                NewsletterUpdate(user_id=user_tg_id, document=open(file_path, 'rb'))
                )
            order.sent_to_provider = True
        except Exception as ex:
            print(f"Failed to send order {order.id} to provider {tg_id}: {ex}")
            await application.bot.send_message(
                chat_id=206261493, 
                text=f"Не удалось отправить заказ {order.id} поставщику {user_tg_id}. Пожалуйста, проверьте настройки.\n{ex}"
                )
            
    # await order.asave()