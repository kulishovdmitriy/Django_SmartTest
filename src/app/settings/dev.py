from app.settings.components.base import * # noqa
from app.settings.components.dev_tools import * # noqa


DEBUG = True

ALLOWED_HOSTS = ['*']

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
        'smart_test': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
