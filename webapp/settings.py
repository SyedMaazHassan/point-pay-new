"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from decouple import config as env

# import urllib.parse as up

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENVIRO = env('enviro')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "e==u0$%jf&(v@_q8m#^3ue%8o^yomj9)pqz+$+#j8izdp=6dcf"

# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRO == "local":
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "map",
    "payment",
    "authentication.apps.AuthenticationConfig",
    "api.apps.ApiConfig",
    "landing.apps.LandingConfig",
    "dashboard.apps.DashboardConfig",
    "drivers.apps.DriversConfig",
    "shuttles.apps.ShuttlesConfig",
    "vouchers.apps.VouchersConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_bootstrap5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "webapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "dashboard.processors.current_base_domain",
                "dashboard.processors.current_user",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "webapp.wsgi.application"


# Jazzmind setting
JAZZMIN_SETTINGS = {
    "site_title": "Admin",
    "site_logo": "logo2.jpg",
    "copyright": "Point Pay Ltd",
    "site_icon": "logo3.png",
    "site_logo_classes": "img-circle",
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# up.uses_netloc.append("postgres")
# db_url = "postgres://nmetkbez:8PAg1gnsk6GEwNR2YI1XPEF3mx-V7F71@castor.db.elephantsql.com/nmetkbez"
# url = up.urlparse(db_url)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'nmetkbez',
#         'USER': 'nmetkbez',
#         'PASSWORD': '8PAg1gnsk6GEwNR2YI1XPEF3mx-V7F71',
#         'HOST': 'castor.db.elephantsql.com'
#     }
# }

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("api.authentication.RequestAuthentication",),
    "EXCEPTION_HANDLER": "api.support.custom_exception_handler",
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Karachi"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


DEFAULT_AUTO_FIELD = "django.db.models.AutoField"



LOGIN_URL = "/dashboard/authentication/login/"
LOGIN_REDIRECT_URL = "/dashboard/"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

BOOTSTRAP5 = {
    "error_css_class": "django_bootstrap5-error",
    "required_css_class": "django_bootstrap5-required",
    "javascript_in_head": True,
    "layout": "floating",
}


PAYMENT_SESSION_EXPIRY_MIN = 4
CURRENCY_SYMBOL = "Rs"
POINTPAY_FEE = 0


LOCALHOST = env("localhost")
LIVEHOST = env("livehost")

STRIPE = {
    'publishableKey': env("publishableKey"),
    'secretKey': env("secretKey")
}
