from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
import requests
from django.template import loader
from django.views.decorators.http import require_POST

from .models import TutorClass, Tutor, Classes_with_tutors, Session_Request, Student
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
import json
from django.core.mail import send_mail, EmailMessage


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
        #uppercase query for subject searching
        query = query.upper()
        #Try searching by subject
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
        # uppercase query for subject searching
        query = query.upper()
        # Try searching by subject
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

        return render(request, 'tutor.html', context)
    else:
        return render(request, 'tutor.html')


def tutor_hours(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        rate = request.POST.get('rate')
        tutoring_type = request.POST.get('tutoring_type')
        days = request.POST.getlist('days[]')
        days_str = ", ".join(days)

        tutor_class = TutorClass(
            class_name=class_name,
            tutor=request.user.username,
            rate=rate,
            start_time=start_time,
            end_time=end_time,
            tutoring_type=tutoring_type,
            days=days_str,
        )

        tutor_class.save()

        messages.success(request, 'Tutoring hours added successfully!')
        return render(request, 'tutor_hours.html')

    return render(request, 'tutor_hours.html')


def student_request_confirmation(request, course_name):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        print(class_name)
        tutor_for_session = request.POST.get('tutor')
        print(tutor_for_session)
        stud = request.user.username
        print(stud)

        session_request = Session_Request(
            class_name=class_name,
            tutor_for_session=tutor_for_session,
            student=stud,
            email=request.user.email
        )
        session_request.save()
        print(session_request.email)
        #return render(request, 'request_submitted.html', {'class_name' : class_name, 'tutor_for_session': tutor_for_session, 'student': stud})
        return redirect('student_home')
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
        subject = request.POST.get('course_subject')
        class_number = request.POST.get('course_catalog_nbr')
        full_name = str(subject) + " " + str(class_number)
        print(full_name)

        if full_name:
            tutor_classes = TutorClass.objects.filter(class_name=full_name)
        else:
            tutor_classes = TutorClass.objects.all()
    else:
        tutor_classes = TutorClass.objects.all()
    return render(request, 'sign_up.html', {'tutor_classes': tutor_classes})


@login_required
def tutor_home(request):
    # tutor_classes = TutorClass.objects.filter(tutor=request.user)
    tutor_classes = TutorClass.objects.filter(tutor=request.user.username)
    Session_Requests = Session_Request.objects.filter(tutor_for_session=request.user.username)
    # tutor_requests = TutorRequest.objects.filter(tutor=request.user).select_related('student', 'tutor_class')
    context = {'tutor_classes': tutor_classes, 'session_requests': Session_Requests}
    return render(request, 'tutor_home.html', context)

@login_required
def student_home(request):
    # tutor_classes = TutorClass.objects.filter(tutor=request.user)
    #tutor_classes = TutorClass.objects.filter(tutor=request.user.username)
    Session_Requests = Session_Request.objects.filter(student=request.user.username)
    # tutor_requests = TutorRequest.objects.filter(tutor=request.user).select_related('student', 'tutor_class')
    context = {'session_requests': Session_Requests}
    return render(request, 'student_home.html', context)

@login_required
@require_POST
def delete_request(request):
    student = request.POST['student']
    class_name = request.POST['class_name']
    Session_Request.objects.filter(student=student, class_name=class_name).delete()
    return redirect('student_home')


@login_required
def update_availability(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        new_rate = request.POST.get('rate')
        tutoring_type = request.POST.get('tutoring_type')
        days = request.POST.get('days')

        tutor_class, created = TutorClass.objects.update_or_create(
            class_name=class_name,
            tutor=request.user.username,
            rate=new_rate,
            defaults={
                'start_time': start_time,
                'end_time': end_time,
                'tutoring_type': tutoring_type,
                'days': days
            }
        )

        return redirect('tutor_home')
    else:
        return HttpResponseNotAllowed(['POST'])

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required
def approve_request(request):
    if request.method == 'POST':
        student = request.POST.get('student')
        class_name = request.POST.get('class_name')

        req = Session_Request.objects.filter(
            class_name=class_name,
            student=student,
        )
        for r in req:
            r.status = True
            r.save()

        session_request = Session_Request.objects.get(student=student, class_name=class_name)

        tutor_name = session_request.tutor_for_session
        tutor_email = request.user.email
        student_email = session_request.email

        print(student_email)
        print(tutor_email)
        print(tutor_name)

        send_mail(
            'Session Request Approved',
            f'Hello {student}, your session request for {class_name} has been approved by {tutor_name}. Contact details for the tutor are: Email: {tutor_email}',
            'tutormea24@outlook.com',
            [student_email],
            fail_silently=False,
        )

        return redirect('tutor_home')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def connect(request):
    if request.method == 'POST':
        student = request.POST.get('student')
        class_name = request.POST.get('class_name')

        req = Session_Request.objects.filter(
            class_name=class_name,
            student=student,
        )
        #for r in req:

            #display contact information

        context = {}

        return render(request, 'connect.html', context)
    else:
        return HttpResponseNotAllowed(['POST'])
