from django.contrib import admin

# Register your models here.
from .models import TutorClass, Classes_with_tutors, Tutor, Session_Request

admin.site.register(TutorClass)
admin.site.register(Classes_with_tutors)
admin.site.register(Tutor)
admin.site.register(Session_Request)

