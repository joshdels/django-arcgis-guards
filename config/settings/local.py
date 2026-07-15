from .base import *

SECRET_KEY = "django-insecure-1hj(nx-%cv5=d2@xy&^a&%s^@o@21*zy1z*xo2k6%8o%s$+$x$"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}