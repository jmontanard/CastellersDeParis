from settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'#os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# https://docs.djangoproject.com/en/1.9/howto/static-files/
#  Static files (CSS, JavaScript, Images)

STATIC_ROOT = 'public/static'
STATIC_URL = '/static/'

MEDIA_ROOT = 'public/media'
MEDIA_URL = '/media/'

# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
)
