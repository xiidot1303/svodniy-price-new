from app.services.excel_service import read_excel_and_update_data
from app.models import Excel
from asgiref.sync import async_to_sync, sync_to_async

async def update_excel():
    async for excel in Excel.objects.filter(is_uploaded=False):
        excel: Excel
        excel.is_uploaded = True
        await excel.asave()
        status, error = await sync_to_async(read_excel_and_update_data)(f'files/{excel.file}')
        excel.status = status
        excel.error = error
        await excel.asave()