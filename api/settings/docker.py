from .base import *
import os


DEBUG = os.environ.get("DJANGO_DEBUG", "") == "True"
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', ''),
        'USER': os.environ.get('DB_USERNAME', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}

PREMAILER_OPTIONS = {"base_url": "http://dev.makeaplea.dsd.io",
                     "remove_classes": False,
                     "keep_style_tags": True,
                     "cssutils_logging_level": logging.ERROR}

SMTP_ROUTES["GSI"]["USERNAME"] = os.environ.get("GSI_EMAIL_USERNAME", "")
SMTP_ROUTES["GSI"]["PASSWORD"] = os.environ.get("GSI_EMAIL_PASSWORD", "")
SMTP_ROUTES["PNN"]["USERNAME"] = os.environ.get("PNN_EMAIL_USERNAME", "")
SMTP_ROUTES["PNN"]["PASSWORD"] = os.environ.get("PNN_EMAIL_PASSWORD", "")

BROKER_TRANSPORT_OPTIONS = {'region': 'eu-west-1',
                            'queue_name_prefix': os.environ.get("CELERY_QUEUE_POLLING_PREFIX", "dev-"),
                            'polling_interval': 1,
                            'visibility_timeout': 3600}

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS", "localhost:8000"), ]

# Enable CachedStaticFilesStorage for cache-busting assets
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

CELERY_ALWAYS_EAGER = os.environ.get("CELERY_ALWAYS_EAGER", False)
BROKER_URL = os.environ.get("CELERY_BROKER_URL", "SQS://")

#
# Temporary keys to run collectstatic on docker image build.
#
# Override in your environment.
#
SECRET_KEY = os.environ.get("SECRET_KEY", "46c4b7f21d407686230bbe39ebd8da2834fe2bf2")
ENCRYPTED_COOKIE_KEYS = [
    os.environ.get("ENCRYPTED_COOKIE_KEY", "12fcb4f3db7032b8260fff87074dd29a71128277")
]

STORE_USER_DATA = os.environ.get("STORE_USER_DATA", "") == "True"
