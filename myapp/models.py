from django.db import models
from django.contrib.auth.models import User


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
    # department = models.CharField(max_length=4)
    # course_number = models.IntegerField(max_length=4)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.class_name


class Classes_with_tutors(models.Model):
    class_name = models.CharField(max_length=225)
    class_code = models.ForeignKey(TutorClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_code
