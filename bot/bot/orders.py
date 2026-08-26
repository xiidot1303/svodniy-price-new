from bot.bot import *
from app.services.order_service import *

async def send_orders_list(update: Update, context: CustomContext):
    if update.callback_query:
        await update.callback_query.edit_message_reply_markup(None)

    bot_user: Bot_user = await get_object_by_update(update)
    order_id = context.user_data['order_id']
    order: Order = await Order.objects.aget(pk=order_id)
    # set order by prodivers
    provider_items = {}
    providers = {}
    async for item in OrderItem.objects.filter(order=order):
        provider = await Provider.objects.filter(
            name__contains=item.provider_name.lower()
            ).exclude(tg_id=None).afirst()
        if provider:
            if not provider.id in provider_items:
                provider_items[provider.id] = []    
            provider_items[provider.id].append(item)
            providers[provider.id] = provider
    
    # Prepare text message
    message = f"<b>Заказ №{order.id} | {order.datetime.strftime('%d.%m.%Y')}</b>\n\n"
    for provider_id, items in provider_items.items():
        provider: Provider = providers.get(provider_id)
        operator: Operator = await order.get_operator
        if not operator:
            bot_user_tg_id = provider.tg_id or '0'
        else:
            bot_user_tg_id = operator.tg_id
        
        # get provider username by tg_id if bot user is exist
        if bot_user := await Bot_user.objects.filter(user_id = int(float(bot_user_tg_id))).afirst():
            provider_username = f"""<a href="tg://user?id={bot_user.user_id}">""" \
                f"""{f"@{bot_user.username}" if bot_user.username else bot_user.firstname}</a>"""
        else:
            provider_username = ""

        t = (
            f"<b>🔹 Поставщик: {provider.name}  {provider_username}</b>\n"
            f"📞 {provider.phone}\n\n"
            )
        for idx, item in enumerate(items, start=1):
            t += (
                f"{idx}. {item.title}\n"
                f"   Производитель: {item.manufacturer}\n"
                f"   Страна: {item.country}\n"
                f"   Цена: {item.price}\n"
                f"   Количество: {item.count}\n\n"
            )
        message += t
        message += "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
    
    # set next order id
    next_order: Order = await Order.objects.filter(
        datetime__lt = order.datetime,
        bot_user__user_id = update.effective_user.id
        ).order_by('-datetime').afirst()
    if next_order:
        markup = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    text=await get_word("load more", update),
                    callback_data="load_more_orders"
                )
            ]]
        )
        context.user_data['order_id'] = next_order.id 
    else:
        markup = None
        context.user_data['order_id'] = None 

    await update.effective_message.reply_html(
        text=message,
        reply_markup=markup
    )
    

