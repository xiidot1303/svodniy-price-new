from django.core.management.base import BaseCommand
from app.scheduled_job.uploading_job import update_excel
import asyncio

class Command(BaseCommand):
    help = 'Command that update uploaded excels'

    def handle(self, *args, **options):
        try:
            update_excel()
            print("Success")
        except Exception as ex:
            print(ex)