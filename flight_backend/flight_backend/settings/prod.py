import os
import dj_database_url
from .base import *  # noqa: F403,F401


DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]

DATABASES["default"] = dj_database_url.config(default=os.environ["DATABASE_URL"])
ALLOWED_HOSTS += []  # noqa ignore=F405
