from app.api import *
from app.utils import *
from app.services.drug_service import *
from adrf.views import APIView

class ProviderByName(APIView):
    @swagger_auto_schema(request_body=ProviderFilterSerializer, responses={status.HTTP_200_OK: ProviderSerializer})
    async def post(self, request):
        title = request.data.get('title', None)
        provider: Provider = await get_provider_by_name_contains(title)
        if provider:
            serializer = ProviderSerializer(provider)
            return Response(await serializer.adata, status=status.HTTP_200_OK)
            
        return Response({"error": "No providers found with the given title"}, status=status.HTTP_404_NOT_FOUND)