"""Celery application for asynchronous jobs."""

import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "i3aps_platform.settings.prod")

app = Celery("i3aps_platform")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
