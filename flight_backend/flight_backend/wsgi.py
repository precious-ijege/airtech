"""
WSGI config for flight_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ["ENV"] == "PRODUCTION":
    setting = "flight_backend.settings.prod"
else:
    setting = "flight_backend.settings.dev"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting)

application = get_wsgi_application()
