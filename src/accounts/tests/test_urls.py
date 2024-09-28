from django.test import TestCase, Client
from django.urls import reverse
from colorama import Fore, Style, init


class TestUrls(TestCase):
    """
        TestUrls class is a Django TestCase that verifies the availability of public and authenticated URLs.

        Attributes:
            fixtures: List of fixtures to load initial data for tests.

        Methods:
            setUp:
                Initializes the test client and enables colored output for test results.

            test_urls_accounts_public_availability:
                Verifies that public account URLs (registration and login) are accessible and returns a status code of 200.

            test_urls_accounts_private_authenticated_availability:
                Logs in with admin credentials and verifies that private account URLs (profile) are accessible.
    """

    fixtures = [
        'dump.json'
    ]

    def setUp(self):

        init(autoreset=True)
        self.client = Client()

    def test_urls_accounts_public_availability(self):
        urls = [
            reverse('accounts:registration'),
            reverse('accounts:login')
        ]

        for url in urls:
            response = self.client.get(url)
            if response.status_code == 200:
                print(Fore.GREEN + f'URL {url} доступен' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'URL {url} недоступен, статус: {response.status_code}' + Style.RESET_ALL)
            self.assertEqual(response.status_code, 200)

    def test_urls_accounts_private_authenticated_availability(self):
        urls = [
            reverse('accounts:profile'),
        ]

        self.client.login(username='admin', password='admin')

        for url in urls:
            response = self.client.get(url)

            if response.status_code == 302:
                print(Fore.GREEN + f'URL {url} доступен' + Style.RESET_ALL)
