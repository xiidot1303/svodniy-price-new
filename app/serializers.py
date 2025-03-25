from rest_framework import serializers
from adrf.serializers import Serializer, ModelSerializer
from app.models import *
from bot.models import Bot_user


class DrugListSerializer(ModelSerializer):
    class Meta:
        model = Drug
        fields = ('title', 'title_en', 'term', 'atc')


class DrugFilterSerializer(Serializer):
    title = serializers.CharField(
        required=False, allow_blank=True, max_length=255)


class DrugSerializer(ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'


class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class ProviderFilterSerializer(Serializer):
    name = serializers.CharField(
        required=False, allow_blank=True, max_length=255)


class BotUserSerializer(ModelSerializer):
    class Meta:
        model = Bot_user
        fields = '__all__'


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['title', 'title_en', 'provider_name', 'price', 'manufacturer', 'country', 'count']


class BotUserSerializer(ModelSerializer):
    class Meta:
        model = Bot_user
        fields = ['user_id']


class OrderSerializer(ModelSerializer):
    bot_user = serializers.SlugRelatedField(
        queryset=Bot_user.objects.all(),
        slug_field='user_id'
    )
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['bot_user', 'payment_method', 'order_items']

    async def acreate(self, validated_data):
        items_data = validated_data.pop('order_items')

        # Create the order
        order = await Order.objects.acreate(**validated_data)

        # Add items to the order
        for item_data in items_data:
            item, created = await OrderItem.objects.aget_or_create(order=order, **item_data)

        return order
