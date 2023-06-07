
import os
from pathlib import Path
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from configurations import Configuration
from django.utils import timezone


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


class Dev(Configuration):

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    logs = BASE_DIR / "logs"
    if not logs.exists():
        logs.mkdir()

    # Load the environment
    load_dotenv(BASE_DIR / '.envs')
    load_dotenv(override=True)
    env = os.environ.copy()

    SECRET_KEY = env.get('DJANGO_SECRET_KEY')
    EMAIL_BACKEND = env.get('EMAIL_BACKEND')
    EMAIL_HOST = env.get('EMAIL_HOST')
    EMAIL_HOST_USER = env.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env.get('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = env.get('EMAIL_PORT')
    EMAIL_USE_TLS = env.get('EMAIL_USE_TLS')
    DEFAULT_FROM_EMAIL = env.get('DEFAULT_FROM_EMAIL')
    FIREBASE_AUTH_JSON = env.get('FIREBASE_AUTH_JSON')
    ADMIN_URL = env.get("DJANGO_ADMIN_URL")

    TOKEN_REFRASH_RATE = 604800  # 7 days in seconds

    cred = credentials.Certificate(FIREBASE_AUTH_JSON)
    firebase_admin.initialize_app(cred)

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['*']

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'users',
        'product',
        'observer',
        "graphene_django",
        'django_filters',
        'corsheaders',
        'django_celery_beat',
        'django_celery_results',
        'payments',
    ]

    GRAPHENE = {
        "SCHEMA": "config.root_schema.schema",
        "ATOMIC_MUTATIONS": True,
        'SCHEMA_OUTPUT': 'schema.json',
        'MIDDLEWARE': (
            'graphene_django.debug.DjangoDebugMiddleware',
        ),
    }

    CORS_ALLOW_CREDENTIALS = True

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://192.168.1.101:3000",
        "https://localhost:3000",
        "https://192.168.1.101:3000",
    ]

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'users.middleware.AuthorizationMiddleware',
    ]

    ROOT_URLCONF = 'config.urls'
    ADMIN_URL = "admin/"

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'config.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': env.get('DATABASE_ENGINE'),
            'NAME': env.get('DATABASE_NAME'),
            'USER': env.get('DATABASE_USER'),
            'PASSWORD': env.get('DATABASE_PASSWORD'),
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.Argon2PasswordHasher',
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    ]

    # LOGGING
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # See https://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "mail_admins": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            'info_logs': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': f'{BASE_DIR}/logs/debug-{timezone.now().date()}.log',
            },
            'error_logs': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': f'{BASE_DIR}/logs/error-{timezone.now().date()}.log',
            },
        },
        "root": {"level": "INFO", "handlers": ["console"]},
        "loggers": {
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
            "django.security.DisallowedHost": {
                "level": "ERROR",
                "handlers": ["console", "mail_admins"],
                "propagate": True,
            },
            "error_logger": {
                "level": "ERROR",
                "handlers": ["mail_admins", "error_logs", ],
                "propagate": True,
            },
            "info_logger": {
                "level": "INFO",
                "handlers": ["mail_admins", "info_logs", ],
                "propagate": True,
            },
        },
    }

    # Internationalization
    # https://docs.djangoproject.com/en/3.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/

    STATIC_URL = '/static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    AUTH_USER_MODEL="users.User"


    # CELERY STUFF
    CELERY_ENABLE_UTC = True
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
    CELERY_CACHE_BACKEND = 'default'
    CELERY_RESULT_EXTENDED = True
    CELERY_ACCEPT_CONTENT = ["application/json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = TIME_ZONE
    # SET worker_hijack_root_logger TO FALSE TO SEE LOGS
    CELERY_WORKER_HIJACK_ROOT_LOGGER = False

    # https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html?highlight=crontab#crontab-schedules
    # CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
    CELERY_BEAT_SCHEDULE = {}

    # Twilio Configs
    TWILIO_ACCOUNT_SID = env.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = env.get("TWILIO_AUTH_TOKEN")
    TWILIO_DEFAULT_SENDER = env.get('TWILIO_DEFAULT_SENDER')

    # Stripe Configs
    STRIPE_SECRET = env.get('STRIPE_SECRET')
    STRIPE_KEY = env.get('STRIPE_KEY')
    STRIPE_WEBHOOK_URL = env.get('STRIPE_WEBHOOK_URL')

class Prod(Dev):
    DEBUG = False

    True
    CELERY_BROKER_URL = "redis://redis:6379"
    CELERY_RESULT_BACKEND = "redis://redis:6379"
