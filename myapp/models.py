from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.forms import ModelForm, widgets

#Create your models here.

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class TutorClass(models.Model):
    class_name = models.CharField(max_length=255)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.class_name

