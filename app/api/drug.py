from app.api import *
from app.utils import *
from app.services.drug_service import *
from adrf.views import APIView
from swagger.schemas import *

class DrugListView(APIView):
    @swagger_auto_schema(request_body=DrugFilterSerializer, responses={status.HTTP_200_OK: DrugListSerializer(many=True)})
    async def post(self, request, *args, **kwargs):
        # Get the title from the POST request
        filter_serializer = DrugFilterSerializer(data=request.data)
        if filter_serializer.is_valid():
            title = filter_serializer.validated_data.get('title', None)
            words, text_en, text_ru, text = await prepare_drug_words(title)
            drugs = await sync_to_async(filter_drugs_by_title_regex)(words, text_en, text_ru, text)

            # Serialize the data
            serializer = DrugListSerializer(drugs, many=True)

            return Response(await serializer.adata, status=status.HTTP_200_OK)

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
