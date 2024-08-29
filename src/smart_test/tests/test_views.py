from django.test import TestCase, Client
from django.urls import reverse

from smart_test.models import Test


class TestDetailsViews(TestCase):
    fixtures = [
        'dump.json'
    ]
    TEST_ID = 1

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_details(self):
        response = self.client.get(reverse('tests:details', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context_data.get('test'))

    def test_basic_flow(self):
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

    fixtures = [
        'dump.json'
    ]

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_next_is_redirected_to_details(self):
        response = self.client.get(reverse('tests:next', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('tests:details', kwargs={'id': 1}))

        response = self.client.post(reverse('tests:next', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('tests:details', kwargs={'id': 1}))
