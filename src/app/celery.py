import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"app.settings.{os.environ.get('RUN_MODE', 'staging')}")

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
