# celery.py
import os
from celery import Celery

# Установка переменной окружения с именем проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shope.settings')

app = Celery('shope')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

