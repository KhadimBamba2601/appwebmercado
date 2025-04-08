# datos_externos/scraper_settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = 'django-insecure-wv^ss)@mbmglh=a+2ccs_9vlpdp%!xr3v9l#3&gs%$7^m3fp$^'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'analisis_mercado',  # Ajustado para reflejar la ubicación real
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestion_tareas_db',
        'USER': 'postgres',
        'PASSWORD': 'postgresql',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=public'
        },
        'ATOMIC_REQUESTS': True,
    }
}

AUTH_USER_MODEL = 'auth.User'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'