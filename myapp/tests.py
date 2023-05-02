from django.test import TestCase
from django.utils import timezone
from django.test import Client
from django.urls import reverse
from django.test import TestCase
from myapp.models import Session_Request, TutorClass

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


# class UpdateAvailabilityTestCase(TestCase):
#     def test_update_availability(self):
#         response = self.client.get(reverse('update_availability'))
#         self.assertEqual(response.status_code, 302)
#
#
#


class SessionRequestModelTest(TestCase):

    def setUp(self):
        self.session_request = Session_Request.objects.create(
            class_name='Probability',
            tutor_for_session='Jimmy',
            student='Glory',
            email='gex7ys@virginia.edu',
            status=False
        )

    def test_session_request_creation(self):
        self.assertEqual(self.session_request.class_name, 'Probability')
        self.assertEqual(self.session_request.tutor_for_session, 'Jimmy')
        self.assertEqual(self.session_request.student, 'Glory')
        self.assertEqual(self.session_request.email, 'gex7ys@virginia.edu')
        self.assertFalse(self.session_request.status)

    def test_delete_request(self):
        initial_count = Session_Request.objects.count()
        self.session_request.delete_request()
        self.assertEqual(Session_Request.objects.count(), initial_count - 1)


class TutorClassModelTest(TestCase):
    def setUp(self):
        self.tutor_class = TutorClass.objects.create(
            class_name='Probability',
            tutor='Jimmy',
            rate=25,
            start_time='08:00:00',
            end_time='10:00:00',
            tutoring_type='in_person',
            days='MWF'
        )

    def test_class_name(self):
        tutor_class = TutorClass.objects.get(id=self.tutor_class.id)
        field_label = tutor_class._meta.get_field('class_name').verbose_name
        self.assertEquals(field_label, 'class name')

    def test_tutor(self):
        tutor_class = TutorClass.objects.get(id=self.tutor_class.id)
        field_label = tutor_class._meta.get_field('tutor').verbose_name
        self.assertEquals(field_label, 'tutor')

    def test_rate(self):
        tutor_class = TutorClass.objects.get(id=self.tutor_class.id)
        field_label = tutor_class._meta.get_field('rate').verbose_name
        self.assertEquals(field_label, 'rate')

    def test_tutoring_type(self):
        tutor_class = TutorClass.objects.get(id=self.tutor_class.id)
        field_label = tutor_class._meta.get_field('tutoring_type').verbose_name
        self.assertEquals(field_label, 'tutoring type')

    def test_days_label(self):
        tutor_class = TutorClass.objects.get(id=self.tutor_class.id)
        field_label = tutor_class._meta.get_field('days').verbose_name
        self.assertEquals(field_label, 'days')

    def test_object_name_is_class_name(self):
        tutor_class = TutorClass.objects.get(id=self.tutor_class.id)
        expected_object_name = f'{tutor_class.class_name}'
        self.assertEquals(expected_object_name, str(tutor_class))


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
