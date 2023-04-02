# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.forms import ModelForm, widgets


# Create your models here.

class DateInput(forms.DateInput):
    input_type = 'date'


class StudentProfile(models.Model):
    user = models.OneToOneField
    student_id = models.IntegerField(null=True, blank=True)


class TutorSession(models.Model):
    department = models.CharField(max_length=4)
    course_number = models.CharField(max_length=4)
    date_of_session = widgets.DateInput(attrs={'type': 'date'})
    email = models.EmailField()
    tutor_Name = models.CharField(max_length=30)

    def __str__(self):
        return self.title
