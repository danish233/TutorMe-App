from django.test import TestCase
from django.urls import reverse, resolve
from views import index, student, tutor
from django.utils import timezone

# Create your tests here.
class TestModelTests(TestCase):
    def test_test_systems(self):
        """
        Test case used for github CI/CD actions testing
        """
        self.assertIs(True, True)

    def test_accounts_URls(self):
        url = reverse('index')
        print(resolve(url))

