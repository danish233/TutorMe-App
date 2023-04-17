from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.forms import ModelForm, widgets

#Create your models here.

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username if self.user else ''

class TutorClass(models.Model):
    class_name = models.CharField(max_length=255)
    tutor = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.class_name



