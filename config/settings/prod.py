# prod.py
import json

from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()
]

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "OPTIONS": json.loads(os.getenv("DATABASE_OPTIONS", "{}")),
    }
}

CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOWED_ORIGINS = []
CSRF_TRUSTED_ORIGINS = []
