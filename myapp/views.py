from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
import requests
import json


@login_required
def index(request):
    if request.user.groups.filter(name='Student').exists():
        return render(request, 'student.html')
    elif request.user.groups.filter(name='Tutor').exists():
        return render(request, 'tutor.html')
    else:
        spring_2023 = '1232'
        fall_2023 = '1238'

        dept_url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=' + spring_2023 + '&career=UGRD&institutions=UVA01'
        req = requests.get(dept_url)
        name = req.json()['subjects']
        clist = [i['subject'] for i in name]

        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=' + spring_2023
        classes = []
        search_query = request.GET.get('search_query')
        if search_query:
            for s in clist:
                r = requests.get(url + '&subject=' + s + '&page=1')
                for c in r.json():
                    if search_query.lower() in c['descr'].lower() or search_query.lower() in c['catalog_nbr'].lower():
                        class_info = c['catalog_nbr'] + '-' + c['class_section'], c['component'] + c['descr']
                        classes.append(class_info)
        else:
            for s in clist:
                r = requests.get(url + '&subject=' + s + '&page=1')
                for c in r.json():
                    class_info = c['catalog_nbr'] + '-' + c['class_section'], c['component'] + c['descr']
                    classes.append(class_info)

        paginator = Paginator(classes, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'search_query': search_query}
        return render(request, 'index.html', context)


@login_required
def user_type(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'student':
            return redirect('student_dashboard')
        elif user_type == 'tutor':
            return redirect('tutor_dashboard')
    return render(request, 'user_type.html')


@login_required
def student(request):
    spring_2023 = '1232'
    fall_2023 = '1238'

    dept_url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=' + spring_2023 + '&career=UGRD&institutions=UVA01'
    req = requests.get(dept_url)
    name = req.json()['subjects']
    clist = [i['subject'] for i in name]

    url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=' + spring_2023
    classes = []
    search_query = request.GET.get('search_query')
    if search_query:
        for s in clist:
            r = requests.get(url + '&subject=' + s + '&page=1')
            for c in r.json():
                if search_query.lower() in c['descr'].lower() or search_query.lower() in c['catalog_nbr'].lower():
                    class_info = c['catalog_nbr'] + '-' + c['class_section'], c['component'] + c['descr']
                    classes.append(class_info)
    else:
        for s in clist:
            r = requests.get(url + '&subject=' + s + '&page=1')
            for c in r.json():
                class_info = c['catalog_nbr'] + '-' + c['class_section'], c['component'] + c['descr']
                classes.append(class_info)

    paginator = Paginator(classes, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'search_query': search_query}
   # return render(request, 'index.html', context)
    return render(request, 'student.html', context)


@login_required
def tutor(request):
    spring_2023 = '1232'
    fall_2023 = '1238'

    dept_url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=' + spring_2023 + '&career=UGRD&institutions=UVA01'
    req = requests.get(dept_url)
    name = req.json()['subjects']
    clist = [i['subject'] for i in name]

    url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=' + spring_2023
    classes = []
    search_query = request.GET.get('search_query')
    if search_query:
        for s in clist:
            r = requests.get(url + '&subject=' + s + '&page=1')
            for c in r.json():
                if search_query.lower() in c['descr'].lower() or search_query.lower() in c['catalog_nbr'].lower():
                    class_info = c['catalog_nbr'] + '-' + c['class_section'], c['component'] + c['descr']
                    classes.append(class_info)
    else:
        for s in clist:
            r = requests.get(url + '&subject=' + s + '&page=1')
            for c in r.json():
                class_info = c['catalog_nbr'] + '-' + c['class_section'], c['component'] + c['descr']
                classes.append(class_info)

    paginator = Paginator(classes, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'search_query': search_query}
    # return render(request, 'index.html', context)
    return render(request, 'tutor.html', context)

def tutor_hours(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        hours = request.POST.get('hours')
        return render(request, 'tutor_hours.html', {'class_name': class_name, 'hours': hours})