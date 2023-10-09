import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, "staticfiles/js", "sw.js")

SECRET_KEY = "r6v_=h7h(2xpe*c!v2a^sfe$6xn_%s65jer9-ltp_%c^(k@4fe"

DEBUG = True

ALLOWED_HOSTS = ["*"]
SILENCED_SYSTEM_CHECKS = [
    "models.W042",
    "models.W001",
    "models.W003",
    
    "debug_toolbar.staticfiles.W001",
]


INSTALLED_APPS = [
 
    "django.contrib.admin",
    "django_select2",
    "django.contrib.humanize",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "accounts",
    "transactions",
    "sms_services",
    "crispy_forms",
    "crispy_bootstrap4",
    "dateutil",
    "pwa",
    "django_filters",
    "storages",
    "rest_framework",
    "django_htmx",
    "django_extensions",
    "bootstrap_datepicker_plus",
    "import_export",
    "django_cleanup.apps.CleanupConfig",
]


MIDDLEWARE = [
  
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
        },
    },
]

AUTH_USER_MODEL = "accounts.Account"

WSGI_APPLICATION = "app.wsgi.application"


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "repotranstech$quickdb",
        "USER": "repotranstech",
        "PASSWORD": "6811pass",
        "HOST": "repotranstech.mysql.pythonanywhere-services.com",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
}


AUTH_PASSWORD_VALIDATORS = []


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


CRISPY_TEMPLATE_PACK = "bootstrap4"



LOGIN_REDIRECT_URL = "loans"
LOGOUT_REDIRECT_URL = "login"
INTERNAL_IPS = ["127.0.0.1"]

# =====================EMAIL HOSTING==================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'repotranscompany@gmail.com'
EMAIL_HOST_PASSWORD = 'wmpcilxrbmjgveyg'



REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
    ]
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"




CACHES = {
  
    
   "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/dev/shm",
        "TIMEOUT": 50000,
       "OPTIONS": {"MAX_ENTRIES": 8000},
         },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

SELECT2_CACHE_BACKEND = "default"



