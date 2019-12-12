from config.common_settings import *
import os

DEBUG = False

assert SECRET_KEY is not None, ('Please provide DJANGO_SECRET_KEY environment variable with a value')

ALLOWED_HOSTS += [
    os.getenv('DJANGO_ALLOWED_HOSTS')
]

DATABASES['default'].update({
        'NAME'    : os.getenv('DJANGO_DB_NAME'),
        'USER'    : os.getenv('DJANGO_DB_USER'),
        'PASSWORD': os.getenv('DJANGO_DB_PASSWORD'),
        'HOST'    : os.getenv('DJANGO_DB_HOST'),
        'PORT'    : os.getenv('DJANGO_DB_PORT'),
    }
)