from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.forms import ModelForm, widgets
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usernm = models.CharField(max_length=255, default="No Username Found")
    number_of_sessions = models.IntegerField(default=0)
    avg_rating = models.IntegerField(default=11)
    bio = models.CharField(max_length=255, default="Write a short bio about your skills and experience so students can get to know you better!")

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class TutorClass(models.Model):
    class_name = models.CharField(max_length=255)
    tutor = models.CharField(max_length=255)
    rate = models.IntegerField(default=0)
    start_time = models.TimeField()
    end_time = models.TimeField()
    tutoring_type = models.CharField(max_length=20, choices=[('online', 'Online'), ('in_person', 'In Person')])
    days = models.CharField(max_length=100)
    tutor_email = models.EmailField(default='example@example.com')

    def __str__(self):
        return self.class_name

class Session_Request(models.Model):
    """
    This django model is the main access to the data on students tutor session requests and tutors managing their
    request. The model allows for students to submit requests, delete requsts, and tutors to accept or reject the tutor
    session

    class_name : The name of the class for which the session is being requested.
    tutor_for_session : The name of the tutor the student is requesting a session with.
    student : The username of the student making the session request.
    status : A boolean indicating whether the session request has been accepted or rejected by the tutor.
    email : The email address of the student making the session request.
    """
    class_name = models.CharField(max_length=225)
    tutor_for_session = models.CharField(max_length=50)
    student = models.CharField(max_length=225)
    status = models.BooleanField(default=False)
    email = models.EmailField(default='example@example.com')
    session_start_time = models.TimeField(default='00:00')
    length_in_min = models.IntegerField(default=1)
    left_feedback = models.BooleanField(default=False)

    def __str__(self):
        return self.student

    def __str__(self):
        return self.email

    def delete_request(self):
        self.delete()

