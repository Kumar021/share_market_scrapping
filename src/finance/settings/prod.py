from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['mysite.com','localhost', '*',]




# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#postgree database Production uses
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'DB_NAME',
#         'USER' : 'DB_USERNAME',
#         'PASSWORD' : 'DB_PASS',
#         'HOST' : 'HOST_NAME'
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}



  



