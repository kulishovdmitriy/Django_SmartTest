import os # noqa
from app.settings.components.base import * # noqa
from app.settings.components.database import * # noqa
from app.settings.components.email import * # noqa
# from app.settings.components.celery_rabbitmq_config import * # noqa
from app.settings.components.celery_redis_config import * # noqa
from app.settings.components.rest import * # noqa

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

STATIC_ROOT = '/var/www/smart_test/static'

MEDIA_ROOT = '/var/www/smart_test/media'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'accounts': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
