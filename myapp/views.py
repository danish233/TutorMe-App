from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
import requests
from django.template import loader
from .models import TutorClass, Tutor, Classes_with_tutors, Session_Request
from django.shortcuts import render
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
            return redirect('tutor_home')  # update this line
    return render(request, 'user_type.html')


def student(request):
    if 'q' in request.GET:
        query = request.GET['q']
        query = str(query)
        term = '1232'  # replace with appropriate term code
        url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&subject={query}'
        response = requests.get(url)
        data = response.json()
        courses = []
        context = parse(courses, data, query)

        # no courses found, try searching by course number
        if not courses:
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&catalog_nbr={query}'
            response = requests.get(url)
            data = response.json()
            courses = []
            context = parse(courses, data, query)

        # no courses found, try searching by description
        if not courses:
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&keyword={query}'
            response = requests.get(url)
            data = response.json()
            courses = []
            context = parse(courses, data, query)

        return render(request, 'student.html', context)
    else:
        return render(request, 'student.html')


@login_required
def tutor(request):
    if 'q' in request.GET:
        query = request.GET['q']
        query = str(query)
        term = '1232'  # replace with appropriate term code
        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&subject={query}'
        response = requests.get(url)
        data = response.json()
        courses = []
        context = parse(courses, data, query)

        # no courses found, try searching by course number
        if not courses:
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&catalog_nbr={query}'
            response = requests.get(url)
            data = response.json()
            courses = []
            context = parse(courses, data, query)

        # no courses found, try searching by description
        if not courses:
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&keyword={query}'
            response = requests.get(url)
            data = response.json()
            courses = []
            context = parse(courses, data, query)

        return render(request, 'tutor.html', context)
    else:
        return render(request, 'tutor.html')


def tutor_hours(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        tutor_class = TutorClass(
            class_name=class_name,
            tutor=request.user.username,
            start_time=start_time,
            end_time=end_time,
        )

        tutor_class.save()

        return render(request, 'tutor_hours.html',
                      {'class_name': class_name, 'start_time': start_time, 'end_time': end_time})
    else:
        return render(request, 'tutor_home.html')


def student_request_confirmation(request, course_name):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        tutor_for_session = request.POST.get('tutor')

        session_request = Session_Request(
            class_name=class_name,
            tutor_for_session=tutor_for_session,
            student=request.user.username
        )
        session_request.save()
        return render(request, 'request_submitted.html', {'class_name' : class_name, 'tutor_for_session': tutor_for_session})
    else:
        return render(request, 'student.html')


def parse(courses, data, query):
    for c in data:
        if query.lower() in c['subject'].lower() or query.lower() in c['catalog_nbr'].lower() or \
                query.lower() in c['component'].lower() or \
                query.lower() in c['descr'].lower():
            course = {
                'subject': c['subject'],
                'catalog_nbr': c['catalog_nbr'],
                'component': c['component'],
                'descr': c['descr']
            }
            if course not in courses:
                courses.append(course)

    context = {'courses': courses, 'query': query}
    return context


def sign_up_request(request, course_name):
    if request.method == 'POST':
        # Get the value of the course_name parameter
        form_value = request.POST.get('course_name', None)
        if form_value:
            tutor_classes = TutorClass.objects.filter(class_name=form_value)
        else:
            tutor_classes = TutorClass.objects.all()
    else:
        tutor_classes = TutorClass.objects.all()
    return render(request, 'sign_up.html', {'tutor_classes': tutor_classes})


@login_required
def tutor_home(request):
    # tutor_classes = TutorClass.objects.filter(tutor=request.user)
    tutor_classes = Tutor.objects.filter(user=request.user)
    # tutor_requests = TutorRequest.objects.filter(tutor=request.user).select_related('student', 'tutor_class')
    context = {'tutor_classes': tutor_classes}
    return render(request, 'tutor_home.html', context)


@login_required
def update_availability(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        tutor_class, created = TutorClass.objects.update_or_create(
            class_name=class_name,
            #  tutor=request.user,
            defaults={'start_time': start_time, 'end_time': end_time}
        )

        return redirect('tutor_home')
    else:
        return HttpResponseNotAllowed(['POST'])
