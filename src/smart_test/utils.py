from django.shortcuts import get_object_or_404

from smart_test.models import TestResult, Test


def test_result_for_user(user, id):

    return get_object_or_404(
        TestResult,
        user=user,
        state=TestResult.STATE.NEW,
        test=Test.objects.get(id=id)
    )
