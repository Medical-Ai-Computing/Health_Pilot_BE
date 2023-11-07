import os
from celery.schedules import crontab
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthpilot.settings')

app = Celery('healthpilot')
app.config_from_object('django.conf:settings', namespace='CELERY')
# disable UTC so that Celery can use local time
app.conf.enable_utc = False
app.conf.timezone = 'Africa/Addis_Ababa'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {

    'News Craweler': {
        'task': 'client.tasks.crawel_news',
        'schedule': crontab(minute="*/3")
                        },
}
