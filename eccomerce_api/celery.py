import os

from celery import Celery
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eccomerce_api.settings.base")
app = Celery("eccomerce_api")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
