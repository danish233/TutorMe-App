from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests


@login_required
def index(request):
    if request.user.groups.filter(name='Student').exists():
        # return redirect('student_dashboard')
        return render(request, 'student.html')

    elif request.user.groups.filter(name='Tutor').exists():
        # return redirect('tutor_dashboard')
        return render(request, 'tutor.html')

    else:
        spring_2023 = '1232'
        fall_2023 = '1238'

        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=' + spring_2023 + '&page=1'

        r = requests.get(url + '&subject=' + 'MATH')
        classes = []
        for c in r.json():
            class_info = c['catalog_nbr'] + '-' + c['class_section'], c['component'] + c['descr']
            classes.append(class_info)

        context = {'classes': classes}
        return render(request, 'index.html', context)


@login_required
def student(request):
    return render(request, 'student.html')


@login_required
def tutor(request):
    return render(request, 'tutor.html')
