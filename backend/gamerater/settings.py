"""
Django settings for gamerater project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS').split(', ')


# Application definition

INSTALLED_APPS = [
    'api.apps.ApiConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gamerater.urls'

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

WSGI_APPLICATION = 'gamerater.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config("DB_ENGINE"),
        'NAME': config("DB_NAME"),
        'USER' : config("DB_USER"),
        'PASSWORD' : config("DB_PASSWORD"),
        'HOST' : config("DB_HOST"),
        'PORT' : config("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config("DJANGO_TZ")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, config('DJANGO_STATICFILES_DIRS'))]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ORIGIN_WHITELIST_IMPORT = config("CORS_ORIGIN_WHITELIST")
CORS_ORIGIN_WHITELIST = tuple(CORS_ORIGIN_WHITELIST_IMPORT.split(","))

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "OPTIONS",
]

# Authentication
AUTHENTICATION_BACKENDS = [
    'api.auth.DiscordAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.auth.DiscordTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# Logging
DJANGO_LOG_LEVEL = config("DJANGO_LOG_LEVEL")
SERVICES_LOG_LEVEL = config("SERVICES_LOG_LEVEL")
MYSQL_LOG_LEVEL = config("MYSQL_LOG_LEVEL")
CELERY_WORKER_LOG_LEVEL = config("CELERY_WORKER_LOG_LEVEL")
CELERY_BEAT_LOG_LEVEL = config("CELERY_BEAT_LOG_LEVEL")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] [{levelname}] [{name}]: {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'application.log'),
            'backupCount': 5,
            'maxBytes': 10000000,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
        'formatter': 'verbose',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': False,
        },
        'services': {
            'handlers': ['console', 'logfile'],
            'level': SERVICES_LOG_LEVEL,
            'propagate': False,
        },
        'mysql.connector': {
            'level': MYSQL_LOG_LEVEL,
            'handlers': ['console', 'logfile'],
            'propagate': False,
        },
        'celery': {
            'level': CELERY_WORKER_LOG_LEVEL,
            'handlers': ['console', 'logfile'],
            'propagate': False,
        },
        'celery.beat': {
            'level': CELERY_BEAT_LOG_LEVEL,
            'handlers': ['console', 'logfile'],
            'propagate': False,
        },
    },
}

CELERY_BROKER_URL = f'sqla+mysql://{config("DB_USER")}:{config("DB_PASSWORD")}@{config("DB_HOST")}:{config("DB_PORT")}/{config("DB_NAME")}'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_TASK_ACKS_LATE = True