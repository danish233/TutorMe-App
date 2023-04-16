from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Tutor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    computing_id = models.CharField(max_length=8)


class TutorClass(models.Model):
    class_name = models.CharField(max_length=255)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.class_name


class Classes_with_tutors(models.Model):
    class_name = models.CharField(max_length=225)
    class_code = models.ForeignKey(TutorClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_code
