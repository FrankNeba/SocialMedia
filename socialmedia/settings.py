"""
Django settings for socialmedia project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import django_heroku
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_)8-yrfrjf$a9j6^2=-1c=k_tg62f2*ms@&qjt0(yc6k!##0pc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://socialmedia-production-14f4.up.railway.app']



# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authenticate',
    'posts',
    'adminpanel',
    'message',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'socialmedia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'socialmedia.wsgi.application'
ASGI_APPLICATION = 'socialmedia.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}


AUTH_USER_MODEL = 'authenticate.User'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Check if we are on Heroku or a local environment
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',  # Use PostgreSQL on Heroku
            'NAME': os.environ['DATABASE_URL'].split('/')[-1],
            'USER': os.environ['DATABASE_URL'].split(':')[1].split('/')[2],
            'PASSWORD': os.environ['DATABASE_URL'].split(':')[2].split('@')[0],
            'HOST': os.environ['DATABASE_URL'].split('@')[1].split(':')[0],
            'PORT': os.environ['DATABASE_URL'].split(':')[-1],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Local SQLite file
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

TIME_ZONE = 'Africa/Douala'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_ROOT = BASE_DIR / 'static/media'

STATIC_ROOT = BASE_DIR / 'staticfiles'
django_heroku.settings(locals())
# STATICFILES_DIRS = os.path.join(base)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_MAIL = "ngwafranklin29@gmail.com"
EMAIL_HOST_USER ="ngwafranklin29@gmail.com"
EMAIL_HOST_PASSWORD = "lgxw jovy uayr ockb"
