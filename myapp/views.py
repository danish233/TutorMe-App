from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.user.groups.filter(name='Student').exists():
        return redirect('student_dashboard')
    elif request.user.groups.filter(name='Tutor').exists():
        return redirect('tutor_dashboard')
    else:
        return redirect('index')

@login_required()
def student(request):
    return render(request, 'student.html')

@login_required
def tutor(request):
    return render(request, 'tutor.html')