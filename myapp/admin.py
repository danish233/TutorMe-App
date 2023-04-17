from django.contrib import admin

# Register your models here.
from .models import TutorClass, Classes_with_tutors, Tutor

admin.site.register(TutorClass)
admin.site.register(Classes_with_tutors)
admin.site.register(Tutor)