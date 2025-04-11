from pathlib import Path
import os
from . import unfold_settings

# -----------------------------------------------
# BASE SETTINGS
# -----------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")


# -----------------------------------------------
# APPLICATION CONFIGURATION
# -----------------------------------------------

INSTALLED_APPS = [
    # Django Channels
    "channels",
    "daphne",
    # Unfold UI Framework
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    # "unfold.contrib.import_export",
    # "unfold.contrib.guardian",
    # "unfold.contrib.simple_history",
    # Django Default Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Third Party Apps
    "rest_framework",
    # Local Apps
    "reactify",
]

MIDDLEWARE = [
    # Security Middleware
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise Middleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Session and Authentication Middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Third-Party Middleware
    # "corsheaders.middleware.CorsMiddleware",
    # Local Middleware
    # "cantina.middleware.CashierRedirectMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }


# -----------------------------------------------
# DATABASE CONFIGURATION
# -----------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}


# -----------------------------------------------
# AUTHENTICATION & SECURITY
# -----------------------------------------------

CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ["http://localhost"]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# AUTH_USER_MODEL = "authentication.User"

# -----------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Casablanca"
USE_I18N = True
USE_TZ = True


# -----------------------------------------------
# STATIC FILES & MEDIA FILES
# -----------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "public"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# Rest Framework settings
REST_FRAMEWORK = {
    # "Default renderer classes for Rest Framework
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # "authentication.JWTAuthentication.JWTAuthentication",
    ],
}


# -----------------------------------------------
# UNFOLD CONFIGURATION
# -----------------------------------------------

UNFOLD = unfold_settings.UNFOLD


# -----------------------------------------------
# DEFAULT PRIMARY KEY FIELD
# -----------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] [{levelname:<8}] {name}: {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": (
                "DEBUG"  # if os.environ.get("DJANGO_ENV") == "development" else "INFO"
            ),
            "class": "logging.StreamHandler",
            "formatter": (
                "verbose"  # if os.environ.get("DJANGO_ENV") == "development" else "simple"
            ),
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",  # if os.environ.get("DJANGO_ENV") == "development" else "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": (
                "INFO"  # if os.environ.get("DJANGO_ENV") == "development" else "INFO"
            ),
            "propagate": False,
        },
        # "django.request": {
        #     "handlers": ["console"],
        #     "level": "ERROR",
        #     "propagate": False,
        # },
        # You can add additional loggers here if needed
    },
}
