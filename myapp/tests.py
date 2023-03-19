from django.test import TestCase
from django.urls import reverse, resolve
from views import index, student, tutor
from django.utils import timezone
from myapp.models import Test


# Create your tests here.
def setUP(title='test', body='testing'):
    return Test.objects.create(title=title, body=body, created_at=timezone.now())


class TestModelTests(TestCase):
    def test_test_systems(self):
        """
        Test case used for github CI/CD actions testing
        """
        self.assertIs(True, True)

    def test_creation(self):
        t = setUP()
        self.assertTrue(isinstance(t, Test))

    def test_views(self):
        v = self.create_index()
        url = reverse('')
