from config.common_settings import *

DEBUG = True
SECRET_KEY = 'n^envq-8k*&9&@%s6jogj4v_!z*8$=($g^c8z(-y@%nkkji1gc'

DATABASES['default'].update({
        'NAME': 'answerly',
        'USER': 'answerly',
        'PASSWORD': 'development',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
})