import os
from pathlib import Path
from dotenv import load_dotenv
import rq
# from worker import conn
import boto3
import dj_database_url

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'q#br=ggq_)j+c@2zrvr0hpxl+0di(@!l!#3u7gem-dgs0nw#l4')

# SECURITY WARNING: don't run with debug turned on in production
# DEBUG = int(os.environ.get("DEBUG", default=0))
PRODUCTION = bool(os.environ.get("PRODUCTION", False))

ALLOWED_HOSTS = ['reliability-django.herokuapp.com/', 'localhost', '127.0.0.1', '0.0.0.0']

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

if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('NAME', 'postgres'),
            'USER': os.environ.get('USER', 'postgres'),
            'PASSWORD': os.environ.get('PASSWORD', ''),
            'HOST': os.environ.get('HOST', 'hostname'),
            'PORT': os.environ.get('PORT', '5432'),
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

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

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


# Static files (CSS, JavaScript, Images)
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
        'LOCATION': os.getenv('REDIS_URL', 'redis:6379'),
    },
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: PRODUCTION==False,
}

# queue = rq.Queue('default', connection=conn)

s3_conn = boto3.resource(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', None), 
    aws_secret_access_key=os.environ.get('AWS_SECRECT_ACCESS_KEY', None), 
)

BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME', None)
image_bucket = s3_conn.Bucket(BUCKET_NAME)

RQ_SHOW_ADMIN_LINK = False

if PRODUCTION:
    RQ_QUEUES = {
        'default': {
            'HOST': os.environ.get('REDIS_HOST', None),
            'PORT': os.environ.get('REDIS_PORT', None),
            'DB': 0,
            'PASSWORD': os.environ.get('REDIS_PASSWORD', None),
            'DEFAULT_TIMEOUT': 3600,
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


