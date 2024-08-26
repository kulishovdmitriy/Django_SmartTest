from django.test import TestCase, Client
from django.urls import reverse
from colorama import Fore, Style, init


class TestUrls(TestCase):

    fixtures = [
        'dump.json'
    ]

    def setUp(self):

        init(autoreset=True)
        self.client = Client()

    def test_urls_smart_public_availability(self):
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
