import os
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '!DqvOUY=kWjhkaNi2m~Jb12,)=66b=E65jISNn-9s{i5YxUU]9LKvbW;iDso2OmXp-sX$^E2'

ALLOWED_HOSTS = ["*"]

BUILDINGS_PARALELS = {
    1: ["М", "Л"],
    2: ["А", "Б", "В"],
    3: ["Д", "Е", "Р"],
    4: ["З", "И", "К", "С"],
    5: ["Г", "Ю"],
    6: ["Н", "О"]
}

DEBUG = True
SERV = False

LOGIN_URL = "/auth/"
LOGOUT_REDIRECT_URL = None

AUTH_USER_MODEL = 'Accounts.Account'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Accounts',
    'MainApp',
    'SetupApp',
    'PersonalArea',
    'crispy_forms',
    'crispy_bootstrap4',

    "django_extensions",
    'ckeditor',
    'storages',
    'channels',
    'ChatBot',
    'whitenoise.runserver_nostatic',
    'django_user_agents',
    'rest_framework',
    'django_crontab',
    'rest_framework.authtoken',
    #'debug_toolbar'

]
CRONJOBS = [
    ('*/1 * * * *', 'MainApp.cron.my_scheduled_job')
]

APPEND_SLASH=False
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2

}

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
#"debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

ROOT_URLCONF = 'volunteer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates", BASE_DIR / "PersonalArea/templates/old"],
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

WSGI_APPLICATION = 'volunteer.wsgi.application'

ASGI_APPLICATION = 'volunteer.asgi.application'

DATABASES = {
    # 'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': BASE_DIR / 'db.sqlite3',
    # },

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("POSTGRES_NAME",'default_db'),
        'USER': os.environ.get("POSTGRES_USER",'gen_user'),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD",'rokf4g6yp2'),
        'HOST': os.environ.get("POSTGRES_HOST",'92.255.78.119'),
        # 'PORT': '<db_port>',

    }
}
#- POSTGRES_NAME = default_db
#- POSTGRES_USER = gen_user
#- POSTGRES_PASSWORD = rokf4g6yp2
#- POSTGRES_HOST = 92.255.78.119
#

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

# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'

# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = '/setup/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'volunteer.s3_storage.MediaStorage'

AWS_S3_ENDPOINT_URL = 'https://s3.timeweb.com'
AWS_S3_ACCESS_KEY_ID = "cm62321"
AWS_S3_SECRET_ACCESS_KEY = "afe65a4901c296608dc0d940dc1a58af"
AWS_QUERYSTRING_AUTH = False

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": 'channels.layers.InMemoryChannelLayer'
    }
}
ITEMS_FOR_PAGE = 25

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'ivanaksenov2010@mail.ru'
EMAIL_HOST_PASSWORD = 'SeZcYwzd9pxJX2As9niV'
EMAIL_USE_SSL = True
ROLES_PASSWORDS = {
    "admin": "lJ4I393R",
    "director": "Hklu7QLH",
    "head_teacher": "IUi90tP",
    "teacher": "V6y7Jc",
    "psychologist": "7m8n9p",
    "methodist": "K3T7Jc",
}

PROXIES_PATH = BASE_DIR / "proxies.txt"

TOKEN = os.environ.get("TOKEN","0")
