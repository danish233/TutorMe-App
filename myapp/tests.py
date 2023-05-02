from django.test import TestCase
from django.utils import timezone
from django.test import Client
from django.urls import reverse
from .models import TutorClass, Classes_with_tutors, Session_Request

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

class UserTypeTestCase(TestCase):
    def test_user_type(self):
        response = self.client.get(reverse('user_type'))
        self.assertEqual(response.status_code, 302)

class TutorHoursTestCase(TestCase):
    def test_tutor_hours(self):
        response = self.client.get(reverse('tutor_hours'))
        self.assertEqual(response.status_code, 302)

class TutorHomeTestCase(TestCase):
    def test_tutor_home(self):
        response = self.client.get(reverse('tutor_home'))
        self.assertEqual(response.status_code, 302)

class UpdateAvailabilityTestCase(TestCase):
    def test_update_availability(self):
        response = self.client.get(reverse('update_availability'))
        self.assertEqual(response.status_code, 302)

class DeleteRequestTestCase(TestCase):
    def test_delete_request(self):
        response = self.client.get(reverse('delete_request'))
        self.assertEqual(response.status_code, 302)

class ConnectTestCase(TestCase):
    def test_connect(self):
        response = self.client.get(reverse('connect'))
        self.assertEqual(response.status_code, 302)

class ApproveRequestTestCase(TestCase):
    def test_approve_request(self):
        response = self.client.get(reverse('approve_request'))
        self.assertEqual(response.status_code, 302)

class StudentHomeTestCase(TestCase):
    def test_student_home(self):
        response = self.client.get(reverse('student_home'))
        self.assertEqual(response.status_code, 302)



