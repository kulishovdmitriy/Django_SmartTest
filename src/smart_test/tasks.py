import datetime

from celery.app import shared_task

from smart_test.models import TestResult


@shared_task
def cleanup_outdated_test_results():
    """
        Celery shared task to clean up outdated test results.
        It filters and deletes `TestResult` objects which are in the 'NEW' state
        and have not been updated within the last 7 days.

        :return: None
    """

    outdated_tests = TestResult.objects.filter(
        state=TestResult.STATE.NEW,
        write_date__lte=datetime.datetime.now() - datetime.timedelta(seconds=7*24*3600),
    )

    outdated_tests.delete()

    print('Outdated test_results deleted!')
