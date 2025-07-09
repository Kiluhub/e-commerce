from pathlib import Path
import dj_database_url
import os

# Base directory of your project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-u4x*uzd@8es#v=(9for8ppioj3+*n6d2t5bolw8b$wr69mfhdn'
DEBUG = True  # Turn to False in production!
ALLOWED_HOSTS = ['*']  # Later restrict to your domain or Render URL

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',  # your app
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'ecommerce.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'store' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Database (PostgreSQL on Render or fallback SQLite)
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://ecommerce_db_l0gy_user:X2j20Madu3QRmeoBzOF4EBdJ1nLH4Dyx@dpg-d1mj6763jp1c73eumldg-a.oregon-postgres.render.com/ecommerce_db_l0gy',
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static files (CSS, JS)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # ✅ e.g., static/store/style.css
STATIC_ROOT = BASE_DIR / 'staticfiles'    # ✅ collectstatic gathers here

# ✅ Media files (uploads/images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Login redirect
LOGIN_URL = '/login/'

# ✅ Primary key field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
