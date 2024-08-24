from smart_test.models import TestResult, Test


def test_result_for_user(user, id):

    return TestResult.objects.filter(
        user=user,
        state=TestResult.STATE.NEW,
        test=Test.objects.get(id=id)
    )
