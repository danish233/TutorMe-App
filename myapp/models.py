from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.forms import ModelForm, widgets
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
    days = models.CharField(max_length=50)

    def __str__(self):
        return self.class_name


class Classes_with_tutors(models.Model):
    class_name = models.CharField(max_length=225)
    class_code = models.ForeignKey(TutorClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_code

class Session_Request(models.Model):
    class_name = models.CharField(max_length=225)
    tutor_for_session = models.CharField(max_length=50)
    student = models.CharField(max_length=225)
    status = models.BooleanField(default=False)
    email = models.EmailField(default='example@example.com')

    def __str__(self):
        return self.student

    def __str__(self):
        return self.email

    def delete_request(self):
        self.delete()

