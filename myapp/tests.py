from django.test import TestCase
from django.utils import timezone
from django.test import Client

# Create your tests here.
class TestModelTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_test_systems(self):
        """
        Test case used for github CI/CD actions testing
        """
        self.assertIs(True, True)

    def test_redirect_url_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_admin_url_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_url(self):
        response = self.client.get('/accounts/')
        self.assertEqual(response.status_code, 200)