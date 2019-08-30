from __future__ import absolute_import
import os

from django.conf import settings

from celery import Celery

if os.environ.get("ENV") == "PRODUCTION":
    setting = "flight_backend.settings.prod"
else:
    setting = "flight_backend.settings.dev"

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting)
# django.setup()
app = Celery("flight_backend")

app.config_from_object("django.conf:settings")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
