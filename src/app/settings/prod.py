import os # noqa
from app.settings.components.base import * # noqa
from app.settings.components.database import * # noqa
from app.settings.components.email import * # noqa
# from app.settings.components.celery_rabbitmq_config import * # noqa
from app.settings.components.celery_redis_config import * # noqa


DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(':')

STATIC_ROOT = '/var/www/smart_test/static'

MEDIA_ROOT = '/var/www/smart_test/media'
