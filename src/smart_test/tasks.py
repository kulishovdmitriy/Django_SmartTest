import datetime

from celery.app import shared_task

from smart_test.models import TestResult


@shared_task
def cleanup_outdated_test_results():
    outdated_tests = TestResult.objects.filter(
        state=TestResult.STATE.NEW,
        write_date__lte=datetime.datetime.now() - datetime.timedelta(seconds=7*24*3600),
    )

    outdated_tests.delete()

    print('Outdated test_results deleted!')
