"""
Django settings for employee project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@p5sj45=(^$_b=%3^qzs$=tw72j01+6ay076w)6gogwwaj#if7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
NUMBER_GROUPING = 3

EMAIL_HOST = 'smtp.e-business.co.jp'
EMAIL_HOST_USER = 'yangwanjun@e-business.co.jp'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DOMAIN_NAME = 'http://sales.e-business.co.jp'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'eb',
    'eboa',
    'del_data',
    'django_crontab',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'employee.urls'

WSGI_APPLICATION = 'employee.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eb_sales',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
    },

    'bpm_eboa': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bpm_eboa',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
    },
}

DATABASE_ROUTERS = ['employee.db_router.DbRouter']

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
GENERATED_FILES_ROOT = os.path.join(os.path.abspath(os.path.dirname(BASE_DIR)), "eb_sales_files")

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [PROCESS:%(process)d] [%(module)s:%(lineno)s] %(message)s",
            'datefmt': "%Y/%m/%d %H:%M:%S"
        },
    },
    'handlers': {
        'sync_members': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': os.path.join(BASE_DIR, "log/batch/sync_members.log"),
        },
        'member_status': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': os.path.join(BASE_DIR, "log/batch/member_status.log"),
        },
    },
    'loggers': {
        'eb.management.commands.sync_members': {
            'handlers': ['sync_members'],
            'level': 'INFO',
            'propagate': True,
        },
        'eb.management.commands.member_status': {
            'handlers': ['member_status'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

CRONJOBS = [
    ('*/5 * * * *', 'django.core.management.call_command', ['sync_members']),
]
