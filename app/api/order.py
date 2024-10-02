from app.api import *
from app.services.order_service import *
from bot.services import get_object_by_id as get_bot_user_by_id

class CanOrderForFree(APIView):
    @swagger_auto_schema(request_body=user_id_schema, responses=can_order_response)
    async def post(self, request, *args, **kwargs):
        try:
            bot_user = await get_bot_user_by_id(request.data.get('id', None))
        except:
            bot_user = None

        if bot_user:
            bot_user_serializer = BotUserSerializer(bot_user)
            bot_user = bot_user_serializer.instance
            orders_count = await check_count_of_orders_of_bot_user(bot_user)
            if orders_count >= 3:
                r = False
            else:
                r = True
            response = {"response": r}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No user found with the given ID"}, status=status.HTTP_404_NOT_FOUND)

class CreateOrder(APIView):
    @swagger_auto_schema(request_body=OrderSerializer, responses={
        status.HTTP_201_CREATED: "", 
        status.HTTP_400_BAD_REQUEST: ""
        })
    async def post(self, request, *args, **kwargs):
        order_serializer = OrderSerializer(data=request.data)
        if await sync_to_async(order_serializer.is_valid)():
            # create Order by serializer
            await order_serializer.acreate(order_serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

