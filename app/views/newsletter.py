from django.http import JsonResponse
from app.services.order_service import send_order_newsletter, application
from app.api import *


class OrderNewsletterView(APIView):
    async def post(self, request):
        order_id = request.POST.get("order_id")
        application.create_task(send_order_newsletter(order_id))
        return JsonResponse({"status": "ok"})