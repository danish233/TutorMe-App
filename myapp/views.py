from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import requests
import json


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

        dept_url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=' + spring_2023
        req = requests.get(dept_url)
        #name = req.json()['subjects']
        #clist = []
        #for i in name:
            #clist.append(i['subject'])

        clist = ['MATH', 'APMA', 'ENGR']

        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=' + spring_2023
        classes = []
        for s in clist:
            r = requests.get(url + '&subject=' + s + '&page=1')
            for c in r.json():
                class_info = c['catalog_nbr'] + '-' + c['class_section'], c['component'] + c['descr']
                classes.append(class_info)

        paginator = Paginator(classes, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        #context = {'classes': classes}
        return render(request, 'index.html', context)


@login_required
def student(request):
    return render(request, 'student.html')


@login_required
def tutor(request):
    return render(request, 'tutor.html')
