import logging
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

app = Celery("abonchain.arbitrage")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    logging.info("Request: ")
