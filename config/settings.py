
"""
Django settings for Dokandar project.
"""

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# 1. SECURITY SETTINGS
# =====================================================

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-development-only-key"
)

if not DEBUG and SECRET_KEY.startswith("django-insecure-"):
    raise ImproperlyConfigured(
        "Set a secure DJANGO_SECRET_KEY for production."
    )


# Allowed hosts

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]

# Automatically allow Render's assigned hostname

RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)


# CSRF trusted origins

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS", ""
    ).split(",")
    if origin.strip()
]

if RENDER_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(
        f"https://{RENDER_HOSTNAME}"
    )


# Production HTTPS security

if not DEBUG:

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https"
    )

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 3600


# =====================================================
# 2. APPLICATION DEFINITION
# =====================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'orders',
    'products',
    'accounts',
    'rest_framework',
    'cart',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'


# =====================================================
# 3. TEMPLATES
# =====================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / 'templates'],

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


WSGI_APPLICATION = 'config.wsgi.application'


# =====================================================
# 4. DATABASE CONFIGURATION
# =====================================================

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:

    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }

else:

    # Local development database

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# =====================================================
# 5. PASSWORD VALIDATION
# =====================================================

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


# =====================================================
# 6. INTERNATIONALIZATION
# =====================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True


# =====================================================
# 7. STATIC FILES CONFIGURATION
# =====================================================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# =====================================================
# 8. EMAIL CONFIGURATION (DJANGO 6.1)
# =====================================================

if DEBUG:

    # Development: print emails in terminal

    MAILERS = {
        "default": {
            "BACKEND": "django.core.mail.backends.console.EmailBackend",
        },
    }

else:

    # Production: SMTP email backend

    MAILERS = {
        "default": {
            "BACKEND": "django.core.mail.backends.smtp.EmailBackend",

            "OPTIONS": {
                "host": os.environ.get(
                    "EMAIL_HOST", "smtp.gmail.com"
                ),

                "port": int(
                    os.environ.get("EMAIL_PORT", "587")
                ),

                "username": os.environ.get(
                    "EMAIL_HOST_USER", ""
                ),

                "password": os.environ.get(
                    "EMAIL_HOST_PASSWORD", ""
                ),

                "use_tls": True,
            },
        },
    }

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "webmaster@localhost"
)


# =====================================================
# 9. CUSTOM USER MODEL
# =====================================================

AUTH_USER_MODEL = 'accounts.CustomUser'


# =====================================================
# 10. DJANGO REST FRAMEWORK
# =====================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# =====================================================
# 11. AUTHENTICATION SETTINGS
# =====================================================

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"


# =====================================================
# 12. MEDIA FILES
# =====================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# =====================================================
# 13. DEFAULT PRIMARY KEY
# =====================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
