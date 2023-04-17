"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path, include
from django.contrib.auth.views import LogoutView
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', TemplateView.as_view(template_name="index.html")),
    #path('index/', views.index, name='index'),
    #path('', views.index, name='index'),
    path('', views.user_type, name='user_type'),
    path('accounts/', include('allauth.urls')),
    path('accounts/google/student/', views.student, name='student_dashboard'),

    path('accounts/google/student/session_signup/<str:course_name>/', views.sign_up_request, name='session_signup'),
    path('accounts/google/tutor/', views.tutor, name='tutor_dashboard'),
    path('accounts/google/tutor/tutor_hours/', views.tutor_hours, name='tutor_hours'),
    path('accounts/google/tutor/home/', views.tutor_home, name='tutor_home'),
    path('accounts/google/tutor/update_availability/', views.update_availability, name='update_availability'),
    path('logout/', LogoutView.as_view()),

]
