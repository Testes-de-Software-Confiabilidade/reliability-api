import os
from pathlib import Path
from dotenv import load_dotenv
import rq
# from worker import conn
import boto3
import dj_database_url
import dj_redis_url

load_dotenv(dotenv_path='.env', verbose=True, override=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production
DEBUG = True if int(os.environ.get("DEBUG"))==1 else False
PRODUCTION = True if int(os.environ.get("PRODUCTION"))==1 else False

# REMOVE LATER
# DEBUG = False
# PRODUCTION = False
# print('\n'*3)
# print(' DEBUG', DEBUG)
# print('PRODUCTION', PRODUCTION)
# print('\n'*3)

ALLOWED_HOSTS = ['reliability-django.herokuapp.com', 'localhost', '127.0.0.1', '0.0.0.0']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_rq',
    'debug_toolbar',
    'repository',
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

if PRODUCTION == True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('AWS_POSTGRES_DATABASE_NAME', 'postgres'),
            'USER': os.environ.get('AWS_POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('AWS_POSTGRES_PASSWORD', ''),
            'HOST': os.environ.get('AWS_POSTGRES_HOST', 'hostname'),
            'PORT': os.environ.get('AWS_POSTGRES_PORT', '5432'),
            "OPTIONS": {
                "sslmode": "verify-ca",
                "sslrootcert": os.path.join(BASE_DIR, "amazon-rds-ca-cert.pem")
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'reliability',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
        }
    }

# db_from_env = dj_database_url.config(conn_max_age=600)
# DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, 'media')

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        # By default use Docker Compose Redis instance.
        'LOCATION': os.environ.get('REDIS_URL', 'redis:6379'),
    },
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}

if PRODUCTION:
    BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME', None)
    s3_conn = boto3.resource(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', None), 
        aws_secret_access_key=os.environ.get('AWS_SECRECT_ACCESS_KEY', None), 
    )
    image_bucket = s3_conn.Bucket(BUCKET_NAME) if BUCKET_NAME else None
else:
    image_bucket = BUCKET_NAME = None

IMGUR_CLIENT_ID = os.environ.get('IMGUR_CLIENT_ID', None)


RQ_SHOW_ADMIN_LINK = False

if PRODUCTION == True:
    REDIS_URL = os.environ['REDIS_URL']
    REDIS_CONN = dj_redis_url.parse(REDIS_URL)
    RQ_QUEUES = {
        'default': {
            'HOST': REDIS_CONN['HOST'],
            'PORT': REDIS_CONN['PORT'],
            'DB': 0,
            'PASSWORD': REDIS_CONN['PASSWORD'],
            'DEFAULT_TIMEOUT': 7200,
        },
    }
else:
    RQ_QUEUES = {
        'default': {
            'HOST': 'redis',
            'PORT': 6379,
            'DB': 0,
            'DEFAULT_TIMEOUT': 3600,
        },
    }


# import django_heroku
# django_heroku.settings(locals())