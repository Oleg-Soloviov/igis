from myproject.settings import *

DEBUG = False

ALLOWED_HOSTS = ['udm.med.conoto.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'igis_udm',
    }
}
