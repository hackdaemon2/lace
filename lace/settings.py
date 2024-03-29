"""
Django settings for lace project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from decouple import (config, Csv)
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, 'lace')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default = False, cast = bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast = Csv())


# Application definition

INSTALLED_APPS = [
    'user_auth',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'dashboard',
    # 'pwa', #installs app support for progressive web apps
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    # It only formats user lockout messages and renders Axes lockout responses
    # on failed user authentication attempts from login views.
    # If you do not want Axes to override the authentication response
    # you can skip installing the middleware and use your own views.
]

ROOT_URLCONF = 'lace.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'), # this is to load the custom 404 error page
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', 
            ],
        },
    },
]

WSGI_APPLICATION = 'lace.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST'),   # Or an IP Address that your DB is hosted on
        'PORT': config('PORT', cast = int),
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'staticfiles')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATICFILES_FINDER = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder'
]

STATICFILES_DIR = [
    os.path.join(BASE_DIR, 'static'), # general static file dirs not tied to any app
    os.path.join(PROJECT_DIR, 'staticfiles'),
]

# Media directory settings for file uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 900

# Authentication configurations
# LOGIN_URL = 'auth:login'
# LOGOUT_URL = 'auth:logout'
# LOGIN_REDIRECT_URL = 'dashboard:dashboard'
# LOGOUT_REDIRECT_URL = 'auth:login'

# Django-allauth config
# ACCOUNT_AUTHENTICATION_METHOD = 'mobile_number'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 900

AUTH_USER_MODEL = 'user_auth.User'

# Email configurations
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# locale path dirs
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# axes config
# from datetime import timedelta
# SILENCED_SYSTEM_CHECKS = ['axes.W003']
# AXES_FAILURE_LIMIT = 3
# AXES_LOCK_OUT_AT_FAILURE = True
# AXES_RESET_ON_SUCCESS = True
# AXES_COOLOFF_TIME = timedelta(minutes=15)
# AXES_LOCKOUT_TEMPLATE = 'auth/lockout.html'
# AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True

# config for progressive web app support
# PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'templates', 'serviceworker.js')
# PWA_APP_NAME = config('APP_NAME').upper()
# PWA_APP_DESCRIPTION = config('APP_DESCRIPTION')
# PWA_APP_THEME_COLOR = '#0A0302'
# PWA_APP_BACKGROUND_COLOR = '#ffffff'
# PWA_APP_DISPLAY = 'standalone'
# PWA_APP_SCOPE = '/'
# PWA_APP_ORIENTATION = 'any'
# PWA_APP_START_URL = '/'
# PWA_APP_FETCH_URL =  '/'
# PWA_APP_ICONS = [
#   {
#         "src": "/media/icons/android-icon-144x144.png",
#         "sizes": "144x144",
#         "type": "image/png",
#         "density": "0.75"
#   }, 
#   {
#         "src": "/media/icons/android-icon-48x48.png",
#         "sizes": "48x48",
#         "type": "image/png",
#         "density": "1.0"
#   },
#   {
#         "src": "/media/icons/android-icon-72x72.png",
#         "sizes": "72x72",
#         "type": "image/png",
#         "density": "1.5"
#   },
#   {
#         "src": "/media/icons/android-icon-96x96.png",
#         "sizes": "96x96",
#         "type": "image/png",
#         "density": "2.0"
#   },
#    {
#         "src": "/media/icons/android-icon-512x512.png",
#         "sizes": "512x512",
#         "type": "image/png",
#         "density": "6.0"
#   }
# ]
# PWA_APP_SPLASH_SCREEN = [
#     {
#         'src': '/media/icons/android-icon-512x512.png',
#         'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
#     }
# ]
# PWA_APP_DIR = 'ltr'
# PWA_APP_LANG = 'en-US'

# application specific configurations
APP_NAME = config('APP_NAME')
DEVELOPER_NAME = config('DEVELOPER_NAME')
SUPPORT_EMAIL = config('SUPPORT_EMAIL')
SUPPORT_PHONE = config('SUPPORT_PHONE')
ADDRESS = config('ADDRESS')
