from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from app.scheduled_job import uploading_job as uploading, order_job as order
from asgiref.sync import async_to_sync

class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    scheduler.add_job(
        uploading.update_excel, 
        'interval', 
        minutes=10
        )
    scheduler.add_job(
        async_to_sync(order.send_order_notifications), 
        'interval', 
        minutes=2
        )
    
