from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from app.services.order_service import send_order_newsletter
import asyncio
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Order)
def order_created_signal(sender, instance, created, **kwargs):
    """
    This signal is triggered when a new Order is created.
    """
    if created:
        async_to_sync(send_order_newsletter)(instance)