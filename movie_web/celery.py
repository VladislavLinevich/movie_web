import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_web.settings.dev')

app = Celery('movie_web')
app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'send-mail-every-day-at-8': {
        'task': 'movie.tasks.send_mail_func',
        'schedule': crontab(hour=8, minute=0)
    }
    
}

app.autodiscover_tasks()
