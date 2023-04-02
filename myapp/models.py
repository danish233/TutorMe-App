
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
    student_id = models.IntegerField(null=True, blank= True)


class tutorSession(forms.ModelForm):

    department = models.CharField(max_length=4)
    course_number = models.CharField(max_length=3, type=int)
    date_of_session = widgets.DateInput(attrs={'type':'date'})


