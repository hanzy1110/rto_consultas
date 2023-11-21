"""
Django settings for rto_consultas project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# VEHICULAR_UNC
MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PORT = os.environ["MYSQL_PORT"]
MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_ROOT_PASSWORD = os.environ["MYSQL_ROOT_PASSWORD"]

MYSQL_RN_HOST = os.environ["MYSQL_HOST"]
MYSQL_RN_USER = os.environ["MYSQL_USER"]
MYSQL_RN_PORT = os.environ["MYSQL_RN_PORT"]
MYSQL_RN_DATABASE = os.environ["MYSQL_RN_DATABASE"]
MYSQL_RN_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_RN_ROOT_PASSWORD = os.environ["MYSQL_ROOT_PASSWORD"]

POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
RTO_CONSULTAS_DIR = Path(__file__).resolve().parent
RTO_CONSULTAS_RN_DIR = BASE_DIR / "rto_consultas_rn"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = "django-insecure-uecy-2dd!$p*6#0kh!wwgio^sdsoh$v%xiv3yk3ti*=1#w+%2@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False)
ALLOWED_HOSTS = ["*"]

if not DEBUG:
    try:
        SECRET_KEY = os.environ["SECRET_KEY"]
    except KeyError as e:
        raise RuntimeError("Could not find a SECRET_KEY in environment") from e
    # SSL/TLS settings
    ALLOWED_HOSTS = [
        ".52.72.115.11",
        ".rto_consultas_prod",
        "10.0.0.4",
        "10.0.0.3",
        ".rtounco.ddns.net",
    ]
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    # SECURE_SSL_HOST = "localhost"
    SECURE_HSTS_SECONDS = 31536000  # For HSTS (if needed)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # For HSTS (if needed)
    SECURE_HSTS_PRELOAD = True  # For HSTS (if needed)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # SSL Certificate paths
    # SECURE_SSL_CERT = BASE_DIR / "certificates/rto_consultas_prod.crt"
    # SECURE_SSL_KEY = BASE_DIR / "certificates/rto_consultas_prod.key"

# SILKY_PYTHON_PROFILER = True

# Application definition

INSTALLED_APPS = [
    "admin_soft.apps.AdminSoftDashboardConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rto_consultas",
    "rto_consultas_rn",
    "django_tables2",
    "django_htmx",
    "wkhtmltopdf",
    "crispy_forms",
    # "crispy_bootstrap5",
    "crispy_bootstrap4",
    # 'silk'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    # 'silk.middleware.SilkyMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "rto_consultas.urls"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGIN_URL = "accounts/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/logout"

STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # BASE_DIR / 'templates',
            RTO_CONSULTAS_DIR / "templates",
            RTO_CONSULTAS_RN_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "rto_consultas.wsgi.application"
# DATABASE_ROUTERS = 'rto_consultas.db_routers'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": MYSQL_DATABASE,
        "USER": MYSQL_USER,
        "PASSWORD": MYSQL_PASSWORD,
        "HOST": MYSQL_HOST,
        "PORT": MYSQL_PORT,
    },
    "rio_negro": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": MYSQL_RN_DATABASE,
        "USER": MYSQL_RN_USER,
        "PASSWORD": MYSQL_RN_PASSWORD,
        "HOST": MYSQL_RN_HOST,
        "PORT": MYSQL_RN_PORT,
    },
    "users": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": "5432",
    },
}
# ROLE_GROUPS = ["admin", "employee"]

DATABASE_ROUTERS = ["rto_consultas.routers.UserRouter"]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("en", _("English")),
    ("es", _("Spanish")),
]

LANGUAGE_CODE = "es"
LANGUAGE_CODE = "es"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DJANGO_TABLES2_TABLE_ATTRS = {
    "class": "table align-items-center mb-0",
    # 'th': "text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
    # 'thead': {
    #     'class': 'table-light',
    # },
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
PAGINATION = 25
