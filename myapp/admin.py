from django.contrib import admin
from .models import TutorSession, StudentProfile

# Register your models here.
class SessionAdmin(admin.ModelAdmin):
    list_display = ('department', 'course_number', 'date_of_session', 'email','tutor_Name')
    list_filter= ['department']


admin.site.register(TutorSession)