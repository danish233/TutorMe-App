from django.test import TestCase
from django.urls import reverse, resolve
from views import index, student, tutor
from django.utils import timezone
from myapp.models import Test


# Create your tests here.
<<<<<<< Updated upstream
def setUP(title='test', body='testing'):
    return Test.objects.create(title=title, body=body, created_at=timezone.now())


class TestModelTests(TestCase):
=======
class TestURLTests(TestCase):
>>>>>>> Stashed changes
    def test_test_systems(self):
        """
        Test case used for github CI/CD actions testing, and for any setup before other test cases run.
        """
        self.assertIs(True, True)

<<<<<<< Updated upstream
    def test_creation(self):
        t = setUP()
        self.assertTrue(isinstance(t, Test))

    def test_views(self):
        v = self.setUp()
        url = reverse('myapp.views.index')
        resp = self.client.get(url)
        self.assertIn(v.title)





=======
    def test_redirect_url_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_admin_url_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
>>>>>>> Stashed changes
