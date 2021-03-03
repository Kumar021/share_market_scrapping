from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 


ALLOWED_HOSTS = ['localhost', '127.0.0.1',]

INSTALLED_APPS += [
    
]

MIDDLEWARE += [ ]


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'



