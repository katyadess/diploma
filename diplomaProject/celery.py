from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplomaProject.settings')


app = Celery('diplomaProject')
app.conf.enable_utc = False

app.conf.update(timezone = 'Europe/Kiev')

app.config_from_object(settings, namespace='CELERY')


# celery beat settings

app.conf.beat_schedule = {
    'update_pending_to_processing': {
        'task': 'shop.tasks.update_pending_to_processing',
        'schedule': 60.0,
    },
    'update-processing-to-sent-every-day': {
        'task': 'shop.tasks.update_processing_to_sent',
        'schedule': 60.0,
    },
    'update-sent-to-delivered-every-day': {
        'task': 'shop.tasks.update_sent_to_delivered',
        'schedule': 60.0,
    },
    'update-delivered-to-completed-every-day': {
        'task': 'shop.tasks.update_delivered_to_completed',
        'schedule': 60.0,
    },
}

app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    
