from app.models import Evaluation_T, Program_T, Section_T, Student_T
from app.utils import *
from accounts.utils import send_activation_email
from allauth.socialaccount.models import SocialAccount
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required

@login_required(login_url='accounts:login', redirect_field_name='')
def index(request):
    if SocialAccount.objects.filter(user=request.user).exists():
        if not request.user.is_email_verified:
            send_activation_email(request, request.user)
    if not request.user.is_email_verified:
        return redirect('accounts:verify')
    return render(request, 'app/home.html')


def studentcoursewiseplo(request):
    if request.method == 'POST':
        plos = []
        percentage = []
        avgplos = []

        query = getstudentcoursewisePLO(int(request.POST['id']), request.POST['course'])
        for data in query:
            plos.append(data[0])
            percentage.append(data[1])

        query = getcoursewiseavgPLO(request.POST['course'])
        for data in query:
            avgplos.append(data[1])

        return JsonResponse({
            'plos': plos,
            'percentage': percentage,
            'avgplo': avgplos
        })


    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name
    id = 0

    if type == 'Student':
        id = getcorrespondingstudentid(request.user.id)
        id = int(id[0][0])

    context = {
        'name': name,
        'type': type,
        'id': id
    }
    
    return render(request, 'app/coursewiseplo.html', context)

def getstudentcourses(request):
    courses = getcompletedcourses(int(request.GET['id']))

    return JsonResponse({'courses': courses})


def studentprogrmwiseplo(request):
    if request.method == 'POST':
        plos = []
        percentage = []
        avgplos = []

        query = getstudentprogramwisePLO(int(request.POST['id']))
        for data in query:
            plos.append(data[0])
            percentage.append(data[1])
        
        programid = getstudentprogramid(1416455)[0][0]

        query = getprogramwiseavgPLO(programid)
        for data in query:
            avgplos.append(data[1])

        return JsonResponse({
            'plos': plos,
            'percentage': percentage,
            'avgplo': avgplos
        })

    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name
    id = 0

    if type == 'Student':
        id = getcorrespondingstudentid(request.user.id)
        id = int(id[0][0])

    context = {
        'name': name,
        'type': type,
        'id': id
    }

    return render(request, 'app/programwiseplo.html', context)


def PLOacheivementtable(request):
    if request.method == 'POST':
        (plo, courses, table) = getstudentallcoursePLO(int(request.POST['id']), 'report')
        return JsonResponse({'plos': plo, 'courses': courses, 'table': table})





    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    id = 0

    if type == 'Student':
        id = getcorrespondingstudentid(request.user.id)
        id = int(id[0][0])

    context = {
        'name': name,
        'type': type,
        'id': id
    }

    return render(request, 'app/plotable.html', context)

def facultycousewisePLO(request):
    if request.method == 'POST':
        b = request.POST['b']
        e = request.POST['e']
        
        semester =[]
        if b==e:
            semester.append(b)
        elif b == 'Spring 2020' and e == 'Autumn 2020':
            semester=[b,'Summer 2020', e]
        else:
            semester=[b, e]

        (faculty, plonum, plos) = getfacultycoursewisePLO(request.POST['course'].upper(), semester)
        return JsonResponse({
            'plos': plos,
            'plonum': plonum,
            'faculty': faculty
        })
    
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    context = {
        'name': name,
        'type': type,
    }

    return render(request, 'app/facultycoursewiseplo.html', context)


def semestercousewisePLO(request):
    if request.method == 'POST':
        b = request.POST['b']
        e = request.POST['e']
        
        semester =[]
        if b==e:
            semester.append(b)
        elif b == 'Spring 2020' and e == 'Autumn 2020':
            semester=[b,'Summer 2020', e]
        else:
            semester=[b, e]

        (semester, plonum, acheived, failed) = getsemestercoursewisePLO(request.POST['course'].upper(), semester)
        return JsonResponse({
            'acheived': acheived,
            'failed': failed,
            'plonum': plonum,
            'semester': semester
        })
    
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    context = {
        'name': name,
        'type': type,
    }

    return render(request, 'app/semcoursewiseplo.html', context)


def plowisecourseanalysis(request):
    if request.method == 'POST':
        b = request.POST['b']
        e = request.POST['e']
        
        semester =[]
        if b==e:
            semester.append(b)
        elif b == 'Spring 2020' and e == 'Autumn 2020':
            semester=[b,'Summer 2020', e]
        else:
            semester=[b, e]

        plos = request.POST['plos'].split(",")

        (courses, plonum, acheived) = getplowisecoursecomparism(plos, semester)
        return JsonResponse({
            'acheived': acheived,
            'courses': courses,
            'plonum': plonum
        })
    
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    context = {
        'name': name,
        'type': type,
    }

    return render(request, 'app/plowisecoyrseanalysis.html', context)


def semesterwiseploacheivementcntcomp(request):
    if request.method == 'POST':
        b = request.POST['b']
        e = request.POST['e']
        
        semester =[]
        if b==e:
            semester.append(b)
        elif b == 'Spring 2020' and e == 'Autumn 2020':
            semester=[b,'Summer 2020', e]
        else:
            semester=[b, e]

        program = request.POST['program']

        (plonum, new_acheived, new_attempted) = getprogramsemesterwiseplocount(program, semester)
        return JsonResponse({
            'acheived': new_acheived,
            'attempted': new_attempted,
            'plonum': plonum
        })
    
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name
    programs = Program_T.objects.values('programName').distinct()

    new_programs = []

    for program in programs:
        new_programs.append(program['programName'])

    context = {
        'name': name,
        'type': type,
        'programs': new_programs
    }

    return render(request, 'app/semwiseplocnt.html', context)


def programwiseploalnalysisofcourses(request):
    if request.method == 'POST':
        b = request.POST['b']
        e = request.POST['e']
        
        semester =[]
        if b==e:
            semester.append(b)
        elif b == 'Spring 2020' and e == 'Autumn 2020':
            semester=[b,'Summer 2020', e]
        else:
            semester=[b, e]

        program = request.POST['program']

        (plonum, courses, counts) = getprogramwiseploandcourses(program, semester)
        return JsonResponse({
            'courses': courses,
            'counts': counts,
            'plonum': plonum
        })
    
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name
    programs = Program_T.objects.values('programName').distinct()

    new_programs = []

    for program in programs:
        new_programs.append(program['programName'])

    context = {
        'name': name,
        'type': type,
        'programs': new_programs
    }

    return render(request, 'app/progwiseploofcourses.html', context)