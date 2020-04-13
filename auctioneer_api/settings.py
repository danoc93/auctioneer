"""
Django settings for auctioneer_api project.
"""

import os
import auctions.apps
import user_auth.apps

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'xi9c_404kx5g2rt$3o72&_vbtb&1%##_t+x0svpn+fslp=lb21'
DEBUG = os.environ.get('ENV', 'development') != 'production'
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    user_auth.apps.APP_NAME,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    auctions.apps.APP_NAME,
    'oauth2_provider',
    'rest_framework',
    'django_seed',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]

ROOT_URLCONF = 'auctioneer_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates/'],
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

WSGI_APPLICATION = 'auctioneer_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
    },
    'DISPLAY_OPERATION_ID': False,
    'OPERATIONS_SORTER': 'method'
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
)

OAUTH_CLIENT_SECRET = 'fj3C0VJIf5yAXmZB4d3yeSoY2nGmSAKqyMBggpkrweUkvLfDd3S8RnPC2mu2MvV7zCEYNuA5Wgmf9tZDqT3IuFGBhoPdIPaZSFdDcWXnnUZihhR0AZ1gJPtT8rX1ZSr9'
OAUTH_CLIENT_ID = 'bpKXNA1z7hQU9f41MbVdQmaRdj9aiC8ZDNcCT4yM'
OAUTH_TOKEN_URL = 'http://localhost:8000/o/token/'
OAUTH_TOKEN_REVOKE_URL = 'http://localhost:8000/o/revoke_token/'

AUTH_USER_MODEL = "{}.User".format(user_auth.apps.APP_NAME)
