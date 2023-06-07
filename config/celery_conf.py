
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from configurations import importer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

importer.install()

app = Celery('config.celery_conf')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
