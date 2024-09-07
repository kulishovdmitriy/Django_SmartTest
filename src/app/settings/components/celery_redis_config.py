from celery.schedules import crontab


CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULE = {
    'some_task': {
        'task': 'smart_test.tasks.cleanup_outdated_test_results',
        'schedule': crontab(minute='*/50')
    }
}
