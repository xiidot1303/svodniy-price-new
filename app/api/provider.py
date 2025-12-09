from app.api import *
from app.utils import *
from app.services.provider_service import *
from adrf.views import APIView, AsyncRequest
from app.serializers import *
from swagger.responses import *
from bot.services import get_object_by_user_id, Bot_user


class ProviderByName(APIView):
    @swagger_auto_schema(request_body=ProviderFilterSerializer, responses={status.HTTP_200_OK: ProviderSerializer})
    async def post(self, request: AsyncRequest):
        title = request.data.get('name', None)
        provider: Provider = await get_provider_by_name_contains(title)
        if provider:
            serializer = ProviderSerializer(provider)
            return Response(await serializer.adata, status=status.HTTP_200_OK)

        return Response({"error": "No providers found with the given title"}, status=status.HTTP_404_NOT_FOUND)


class ProviderList(APIView):
    @swagger_auto_schema(request_body=ProviderFilterSerializer, responses={status.HTTP_200_OK: ProviderSerializer(many=True)})
    async def post(self, request: AsyncRequest):
        name = request.data.get('name', None)
        filter_serializer = ProviderFilterSerializer(data=request.data)
        if filter_serializer.is_valid():
            name = filter_serializer.validated_data.get('name', None)
            providers = Provider.objects.filter(
                **(await filter_provider_by_name(name))
            )
            serializer = ProviderSerializer(providers, many=True)
            return Response(await serializer.adata, status=status.HTTP_200_OK)
        return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderTgUsernameByName(APIView):
    @swagger_auto_schema(request_body=ProviderFilterSerializer, responses=provider_username_response)
    async def post(self, request: AsyncRequest):
        title = str(request.data.get('name', None)).strip()
        provider: Provider = await get_provider_by_name_contains(title)
        bot_user: Bot_user = (await get_object_by_user_id(round(float(provider.tg_id)))) if provider else None
        username = bot_user.username if bot_user else ""

        return Response({"username": username}, status=status.HTTP_200_OK)


class OperatorByProviderName(APIView):
    @swagger_auto_schema(request_body=OperatorFilterSerializer, responses={status.HTTP_200_OK: OperatorSerializer(many=True)})
    async def post(self, request: AsyncRequest):
        provider_name = str(request.data.get('provider_name', None)).strip()
        filter_serializer = OperatorFilterSerializer(data=request.data)
        if filter_serializer.is_valid():
            operators = Operator.objects.filter(provider__name__icontains = provider_name)
            serializer = OperatorSerializer(operators, many=True)
            return Response(await serializer.adata, status=status.HTTP_200_OK)
        return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        