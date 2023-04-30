from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
import requests
from django.template import loader
from django.views.decorators.http import require_POST

from .models import TutorClass, Tutor, Session_Request, Student
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
import json
from django.core.mail import send_mail, EmailMessage
import time


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

@login_required
def student(request):
    if 'q' in request.GET:
        courses = []
        query = request.GET['q']
        query = str(query)
        term = '1232'  # replace with appropriate term code
        #Try searching by subject + course number
        subandcode = query.upper().split(' ')
        if len(subandcode) == 2:
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&subject={subandcode[0]}&catalog_nbr={subandcode[1]}'
            response = requests.get(url)
            data = response.json()
            context = parse(courses, data, subandcode[0])
        # no courses found, try searching by subject
        if not courses:
            # uppercase query for subject searching (stat vs STAT)
            q = query.upper()
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&subject={q}'
            response = requests.get(url)
            data = response.json()
            context = parse(courses, data, query)

        # no courses found, try searching by course number
        if not courses:
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&catalog_nbr={query}'
            response = requests.get(url)
            data = response.json()
            context = parse(courses, data, query)

        # no courses found, try searching by description
        if not courses:
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&keyword={query}'
            response = requests.get(url)
            data = response.json()
            context = parse(courses, data, query)

        return render(request, 'student.html', context)
    else:
        return render(request, 'student.html')


@login_required
def tutor(request):
    if 'q' in request.GET:
        courses = []
        query = request.GET['q']
        query = str(query)
        term = '1232'  # replace with appropriate term code
        # Try searching by subject + course number
        subandcode = query.upper().split(' ')
        if len(subandcode) == 2:
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&subject={subandcode[0]}&catalog_nbr={subandcode[1]}'
            response = requests.get(url)
            data = response.json()
            context = parse(courses, data, subandcode[0])
        # no courses found, try searching by subject
        if not courses:
            # uppercase query for subject searching (stat vs STAT)
            q = query.upper()
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&subject={q}'
            response = requests.get(url)
            data = response.json()
            context = parse(courses, data, query)

        # no courses found, try searching by course number
        if not courses:
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&catalog_nbr={query}'
            response = requests.get(url)
            data = response.json()
            context = parse(courses, data, query)

        # no courses found, try searching by description
        if not courses:
            url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&keyword={query}'
            response = requests.get(url)
            data = response.json()
            context = parse(courses, data, query)

        return render(request, 'tutor.html', context)
    else:
        return render(request, 'tutor.html')

@login_required
def tutor_hours(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        rate = request.POST.get('rate')
        tutoring_type = request.POST.get('tutoring_type')
        days = request.POST.getlist('days[]')

        days_str = ", ".join(days)

        if days_str == "":
            days_str = "Available All Days"

        tutor_class = TutorClass(
            class_name=class_name,
            tutor=request.user.username,
            rate=rate,
            start_time=start_time,
            end_time=end_time,
            tutoring_type=tutoring_type,
            days=days_str,
            tutor_email = request.user.email
        )
        #prevent duplicate availability slots
        if not TutorClass.objects.filter(class_name=class_name, tutor=request.user.username, rate=rate, start_time=start_time, end_time=end_time, tutoring_type=tutoring_type, days=days_str,):
            tutor_class.save()

        #messages.success(request, 'Tutoring hours added successfully!')
        return render(request, 'tutor_hours.html', {'class_name': class_name, 'start_time': start_time, 'end_time': end_time, 'days_str': days_str, 'tutoring_type': tutoring_type})

    return render(request, 'tutor_hours.html')

@login_required
def student_request_confirmation(request , course_name):
    """
    This function saves the students tutor session request to the database. Based on the class that the student has
    selected from the button, which is the 'POST' request , the session request will be sent to the database and
    the tutor selected and from there the tutors are able to accept or deny the tutor request.
    """

    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        tutor_for_session = request.POST.get('tutor')
        stud = request.user.username
        session_start_time = request.POST.get('session_start_time')
        length_in_min = request.POST.get('length_in_min')


        session_request = Session_Request(
            class_name=class_name,
            tutor_for_session=tutor_for_session,
            student=stud,
            email=request.user.email,
            session_start_time=session_start_time,
            length_in_min=length_in_min
        )

        #TODO: needs to also search by all other tutorclass attributes, otherwise .get() may crash
        info = TutorClass.objects.get(class_name=class_name, tutor=tutor_for_session)

        tutor_name = info.tutor
        tutor_email = info.tutor_email
        student_email = request.user.email
        start = info.start_time
        end = info.end_time
        type = info.tutoring_type
        days = info.days

        if not Session_Request.objects.filter(class_name=class_name, tutor_for_session=tutor_for_session, student=stud, email=request.user.email, session_start_time=session_start_time, length_in_min=length_in_min):
            session_request.save()
            send_mail(
                'New Student Session Request',
                f'Hello {tutor_name}, you have received an {type} session request for {class_name} from student {stud}, from {start} to {end} on {days}. Please login to a24-tutorme.herokuapp.com to approve the request',
                'tutormea24@outlook.com',
                [tutor_email],
                fail_silently=False,
            )

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

@login_required
def sign_up_request(request, course_name):
    """
    This view functions allows users to see the tutors that are available for the classes that they have selected from
    the search page. When the user presses the request session button, this function is called, and it parses through
    Session_Reqeust database in order to find all the available tutors for that specific selected class.
    The function then sends the student to the sign up page where they can select the tutor they would like to request a
    session with.
    """
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

    #make sure tutor has been added to the Tutor class
    tutor = Tutor(
        user=request.user,
        usernm=request.user.username
    )
    if not Tutor.objects.filter(user=request.user, usernm=request.user.username):
        tutor.save()

    me = Tutor.objects.get(user=request.user, usernm=request.user.username)

    context = {'tutor_classes': tutor_classes, 'session_requests': Session_Requests, 'me': me}
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
    """
    This function operates on the students side of the website and allows students to delete a request for a tutoring
     session. The parameter is the HTTP request object that comes from the delete button on the
     student dashboard and when they press that, the function removes the request from the database and then redirects
     the student back to the student home page.

    """
    student = request.POST['student']
    class_name = request.POST['class_name']
    Session_Request.objects.filter(student=student, class_name=class_name).delete()
    return redirect('student_home')

@login_required
@require_POST
def update_bio(request):
    tutor = request.POST['tutor']
    bio = request.POST['bio']
    me = Tutor.objects.get(usernm=tutor)
    me.bio = bio
    me.save()
    return redirect('tutor_home')

@login_required
@require_POST
def view_profile(request):
    tutor = request.POST['tutor_username']
    tutor_ob = Tutor.objects.get(usernm=tutor)
    context = {'tutor': tutor_ob}

    return render(request, 'view_profile.html', context)

@login_required
@require_POST
def leave_rating(request):
    rating = int(request.POST['rating'])
    tutor_for_session = request.POST['tutor_for_session']
    student = request.POST['student']
    class_name = request.POST['class_name']
    session_start_time = request.POST['session_start_time']
    length_in_min = request.POST['length_in_min']


    rated_tutor = Tutor.objects.get(usernm=tutor_for_session)
    if rated_tutor.number_of_sessions == 0:
        #first ever rating
        rated_tutor.avg_rating = rating
        rated_tutor.number_of_sessions = 1
    else:
        rated_tutor.avg_rating = ((rated_tutor.avg_rating * rated_tutor.number_of_sessions) + rating) / (rated_tutor.number_of_sessions + 1)
        rated_tutor.number_of_sessions = rated_tutor.number_of_sessions + 1

    rated_tutor.save()

    Res = Session_Request.objects.filter(tutor_for_session=tutor_for_session, student=student, class_name=class_name, length_in_min=length_in_min)
    for r in Res:
        r.left_feedback = True
        r.save()

    return redirect('student_home')

@login_required
@require_POST
def delete_availability(request):
    class_name = request.POST['class_name']
    tutor = request.POST['tutor']
    rate = request.POST['rate']
    tutoring_type = request.POST['tutoring_type']
    days = request.POST['days']
    TutorClass.objects.filter(tutor=tutor, class_name=class_name, rate=rate, tutoring_type=tutoring_type, days=days).delete()
    return redirect('tutor_home')

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required
def approve_request(request):
    if request.method == 'POST':
        student = request.POST.get('student')
        class_name = request.POST.get('class_name')
        length_in_min = request.POST.get('length_in_min')
        session_start_time = request.POST.get('session_start_time')

        req = Session_Request.objects.filter(
            class_name=class_name,
            student=student,
            length_in_min=length_in_min,
        )
        for r in req:
            r.status = True
            r.save()

            tutor_name = r.tutor_for_session
            tutor_email = request.user.email
            student_email = r.email

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

