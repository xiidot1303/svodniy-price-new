from app.api import *
from app.utils import *
from app.services.provider_service import *
from adrf.views import APIView, AsyncRequest
from app.serializers import *
from swagger.responses import *


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

