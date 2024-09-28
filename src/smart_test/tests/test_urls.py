from django.test import TestCase, Client
from django.urls import reverse
from colorama import Fore, Style, init


class TestUrls(TestCase):
    """
        TestUrls is a test case class that checks the availability of specified URLs for a Django application.

        Inherits from:
            TestCase (django.test)

        Fixtures:
            dump.json: A JSON fixture that loads predefined data into the database.

        Methods:

        setUp:
            Prepares the test client and initializes colorama for colored output. This method is called before each test.

        test_urls_smart_public_availability:
            Tests the availability of public URLs.
            Iterates over a list of public URLs, makes GET requests, and prints the status of each URL with colored output.
                - Green for available (status 200)
                - Red for unavailable (status not 200)

        test_urls_smart_private_authenticated_availability:
            Tests the availability of private URLs for authenticated users.
            Logs in with predefined credentials, iterates over a list of private URLs, makes GET requests, and prints the status
            of each URL with colored output.
                - Green for available (status 200)
                - Yellow for redirects (status 302)
                - Red for unavailable (other status codes)
    """

    fixtures = [
        'dump.json'
    ]

    def setUp(self):
        """
            Set up the testing environment, including initializing the colors with autoreset and
            creating a new Client instance.

            :return: None
        """

        init(autoreset=True)
        self.client = Client()

    def test_urls_smart_public_availability(self):
        """
            Tests the public availability of a list of URLs.

            :return: None
        """

        urls = [
            reverse('tests:list'),
        ]

        for url in urls:
            response = self.client.get(url)
            if response.status_code == 200:
                print(Fore.GREEN + f'URL {url} доступен' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'URL {url} недоступен, статус: {response.status_code}' + Style.RESET_ALL)

    def test_urls_smart_private_authenticated_availability(self):
        """
            Tests the availability of specific URLs for a user who is authenticated. This includes checking if the URLs return
            a status code of 200, 302, or other, and provides corresponding console output for each URL tested.

            :return: None
        """

        urls = [
            reverse('tests:start', args=(1, )),
            reverse('tests:next', args=(1, )),
        ]

        self.client.login(username='admin', password='admin')

        for url in urls:
            response = self.client.get(url)
            if response.status_code == 200:
                print(Fore.GREEN + f'URL {url} доступен' + Style.RESET_ALL)
            elif response.status_code == 302:
                print(Fore.YELLOW + f'URL {url} перенаправляет, статус: {response.status_code}' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'URL {url} недоступен, статус: {response.status_code}' + Style.RESET_ALL)
