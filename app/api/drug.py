from app.api import *
from app.utils import *
from app.services.drug_service import *
from adrf.views import APIView
from rest_framework.pagination import PageNumberPagination
from swagger.schemas import *


class ItemPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = 'page_size'


class DrugListView(APIView):
    pagination_class = ItemPagination

    @swagger_auto_schema(request_body=DrugFilterSerializer, responses=drug_list_response)
    async def post(self, request, *args, **kwargs):
        # Get the title from the POST request
        filter_serializer = DrugFilterSerializer(data=request.data)
        if filter_serializer.is_valid():
            title = filter_serializer.validated_data.get('title', None)
            words, text_en, text_ru, text = await prepare_drug_words(title)
            drugs = await sync_to_async(filter_drugs_by_title_regex)(words, text_en, text_ru, text)

            paginator = self.pagination_class()
            paginated_items = await sync_to_async(paginator.paginate_queryset)(drugs, request, view=self)

            # Serialize the data
            serializer = DrugListSerializer(paginated_items, many=True)

            return Response({
                'next': await sync_to_async(paginator.get_next_link)(),
                'results': await serializer.adata,
            })

        return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DrugListByTitleView(APIView):
    @swagger_auto_schema(request_body=DrugFilterSerializer, responses={status.HTTP_200_OK: DrugSerializer(many=True)})
    async def post(self, request):
        # Get the title from the POST request data
        title = request.data.get('title', None)

        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the drugs by title (case-insensitive search)
        drugs = await filter_drugs_by_title(title)

        if await drugs.aexists():
            # Serialize the filtered drug data
            serializer = DrugSerializer(drugs, many=True)
            return Response(await serializer.adata, status=status.HTTP_200_OK)

        return Response({"error": "No drugs found with the given title"}, status=status.HTTP_404_NOT_FOUND)


class DrugListByProviderView(APIView):
    @swagger_auto_schema(request_body=ProviderFilterSerializer, responses={status.HTTP_200_OK: DrugSerializer(many=True)})
    async def post(self, request):
        # Get the title from the POST request data
        name = request.data.get('name', None)

        if not name:
            return Response({"error": "Provider name is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the drugs by title (case-insensitive search)
        drugs = await filter_drugs_by_provider_name(name)

        if await drugs.aexists():
            # Serialize the filtered drug data
            serializer = DrugSerializer(drugs, many=True)
            return Response(await serializer.adata, status=status.HTTP_200_OK)

        return Response({"error": "No drugs found with the given provider name"}, status=status.HTTP_404_NOT_FOUND)


class DrugInfoView(APIView):
    @swagger_auto_schema(request_body=drug_id_schema, responses={status.HTTP_200_OK: DrugSerializer})
    async def post(self, request):
        id = request.data.get('id', None)
        drug = await get_drug_by_pk(id)
        serializer = DrugSerializer(data=request.data)
        if serializer.is_valid():
            serializer = DrugSerializer(instance=drug)
            return Response(await serializer.adata, status=status.HTTP_200_OK)

        return Response({"error": "No drugs found with the given title"}, status=status.HTTP_404_NOT_FOUND)
