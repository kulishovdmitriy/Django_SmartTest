from django.test import TestCase, Client
from django.urls import reverse

from smart_test.models import Test


class TestDetailsViews(TestCase):
    """
        Unit tests for the `TestDetailsViews` class which handle testing of test details view and basic flow of the test-taking process.

        class TestDetailsViews

        Attributes:
            fixtures (list): Specifies the initial data fixture file to be loaded before the tests.
            TEST_ID (int): Represents a generic test ID used across different test cases.

        Methods:
            setUp(self):
                Initializes the test environment by creating a test client and logging in with admin credentials.

            test_details(self):
                Tests that the details view for a specific test id returns a 200 status code and contains test context information.

            test_basic_flow(self):
                Tests the entire flow of taking a test from start to finish, ensuring proper redirections and form submissions are handled correctly.
    """

    fixtures = [
        'dump.json'
    ]

    TEST_ID = 1

    def setUp(self):
        """
            Sets up the test client and logs in with the credentials of the 'admin' user.

            :return: None
        """

        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_details(self):
        """
            Tests the details view of a specific test instance.

            :return: None
        """

        response = self.client.get(reverse('tests:details', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context_data.get('test'))

    def test_basic_flow(self):
        """
            Tests the basic flow of a Test entity starting from the initial URL to the completion.
            The function simulates the user navigating through each question step by step.

            :return: None
        """

        response = self.client.get(reverse('tests:start', kwargs={'id': self.TEST_ID}))
        self.assertRedirects(response, reverse('tests:next', kwargs={'id': self.TEST_ID}))

        test = Test.objects.get(id=self.TEST_ID)
        questions_count = test.questions.count()

        for step in range(1, questions_count+1):
            next_url = reverse('tests:next', kwargs={'id': self.TEST_ID})
            response = self.client.get(next_url)

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Next')

            response = self.client.post(
                path=next_url,
                data={
                    'form-TOTAL_FORMS': '3',
                    'form-INITIAL_FORMS': '3',
                    'form-MIN_NUM_FORMS': '0',
                    'form-MUX_NUM_FORMS': '1000',
                    'form-0-is_selected': 'on',

                }
            )

            if step < questions_count:
                self.assertRedirects(response, next_url)
            else:
                self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Congratulations!!!')


class TestQuestionView(TestCase):
    """
        TestQuestionView
        ----------------

        A test case class for the 'next' view in the 'tests' application.

        Attributes
        ----------
        fixtures : list
            Contains a list of fixture filenames to load initial data.

        Methods
        -------
        setUp(self):
            Initializes the test client and logs in an admin user before each test.

        test_next_is_redirected_to_details(self):
            Tests that accessing the 'next' view redirects to the 'details' view.
    """

    fixtures = [
        'dump.json'
    ]

    def setUp(self):
        """
            Sets up the test client for the test cases. This method initializes the Client instance
            and logs in using the given credentials.

            :return: None
        """

        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_next_is_redirected_to_details(self):
        """
            Validates that both GET and POST requests to the 'next' view with an id of 1
            result in a redirection to the 'details' view with the same id.

            :return: None
        """

        response = self.client.get(reverse('tests:next', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('tests:details', kwargs={'id': 1}))

        response = self.client.post(reverse('tests:next', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('tests:details', kwargs={'id': 1}))
