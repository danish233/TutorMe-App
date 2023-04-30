from django.contrib import admin

# Register your models here.
from .models import TutorClass, Tutor, Session_Request, Student

admin.site.register(TutorClass)
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Session_Request)

