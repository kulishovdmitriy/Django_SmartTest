from smart_test.models import TestResult, Test


def test_result_for_user(user, id):
    """
        :param user: User object to filter test results.
        :param id: Identifier for the Test object.
        :return: Queryset of TestResult objects that match the given user and test ID, and have the state NEW.
    """

    return TestResult.objects.filter(
        user=user,
        state=TestResult.STATE.NEW,
        test=Test.objects.get(id=id)
    )
