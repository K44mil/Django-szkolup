from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import MyUser, Student, Company
from courses.models import Course
from django.db.models import Q
# Create your views here.

def registerStudent(request):

    msg = ''

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['passwordConfirm']

        if password == confirmPassword:

            try:
                user = MyUser.objects.get(username=username)
            except:
                user = None

            if user is None:
                newUser = MyUser.objects.create_user(
                    username=username,
                    email=username,
                    password=password,
                    role=0,
                )

                newUser.save()

                newStudent = Student.objects.create(
                    email=username,
                    user=newUser,
                )

                newStudent.save()
                return redirect('/')
            else:
                msg = 'Ten adres email jest już zajęty'
        else:
            msg = 'Podane hasła muszą być identyczne'

    context = {
        'msg': msg,
    }

    return render(request, 'registerStudent.html', context)

def registerCompany(request):

    msg = ''

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['passwordConfirm']

        if password == confirmPassword:

            try:
                user = MyUser.objects.get(username=username)
            except:
                user = None

            if user is None:
                newUser = MyUser.objects.create_user(
                    username=username,
                    email=username,
                    password=password,
                    role=1,
                )

                newUser.save()

                newCompany = Company.objects.create(
                    email=username,
                    user=newUser,
                )

                newCompany.save()
                return redirect('/')
            else:
                msg = 'Ten adres email jest już zajęty'
        else:
            msg = 'Podane hasła muszą być identyczne'

    context = {
        'msg': msg,
    }

    return render(request, 'registerCompany.html', context)

def loginView(request):

    msg = ''

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)


        if user is not None:
            login(request, user)

            if not request.user.is_staff:
                if request.user.isProfilEdited == False:
                    if request.user.role == 0:
                        return redirect('/editStudentProfile')
                    elif request.user.role == 1:
                        return redirect('/editCompanyProfile')
                else:
                    return redirect('/')
            return redirect('/')
        else:
            msg = 'Zły adres email lub hasło'

    context = {
        'msg': msg,
    }

    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.isProfilEdited == False:
            if request.user.role == 0:
                return redirect('/editStudentProfile')
            elif request.user.role == 1:
                return redirect('/editCompanyProfile')

    return render(request, 'login.html', context)

def logoutView(request):

    if request.user.is_authenticated:
        logout(request)

    return render(request, 'logout.html', {})

def userProfilView(request):

    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.isProfilEdited == False:
            if request.user.role == 0:
                return redirect('/editStudentProfile')
            elif request.user.role == 1:
                return redirect('/editCompanyProfile')

    return render(request, 'userProfil.html', {})

def editStudentProfileView(request):

    if request.method == 'POST':
        name = request.POST['studentName']
        surname = request.POST['studentSurname']
        city = request.POST['studentCity']
        street = request.POST['studentStreet']
        houseNumber = request.POST['studentHouseNumber']
        flatNumber = request.POST['studentFlatNumber']

        student = Student.objects.get(user=request.user)

        if student is not None:

            # Uzupełnienie danych

            student.name = name
            student.surname = surname
            student.city = city
            student.street = street
            student.house_number = houseNumber
            student.flat_number = flatNumber

            student.save()
            request.user.isProfilEdited = True
            request.user.save()

            return redirect('/')

    return render(request, 'editStudentProfile.html', {})

def editCompanyProfileView(request):

    if request.method == 'POST':
        name = request.POST['companyName']
        city = request.POST['companyCity']
        street = request.POST['companyStreet']
        houseNumber = request.POST['companyHouseNumber']
        flatNumber = request.POST['companyFlatNumber']

        company = Company.objects.get(user=request.user)

        if company is not None:

            # Uzupełnienie danych

            company.company_name = name
            company.city = city
            company.street = street
            company.house_number = houseNumber
            company.flat_number = flatNumber

            company.save()
            request.user.isProfilEdited = True
            request.user.save()

            return redirect('/')

    return render(request, 'editCompanyProfile.html', {})

def studentProfileView(request):

    student = Student.objects.get(user=request.user)

    context = {
        'student': student,
    }

    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.isProfilEdited == False:
            if request.user.role == 0:
                return redirect('/editStudentProfile')
            elif request.user.role == 1:
                return redirect('/editCompanyProfile')

    return render(request, 'studentProfile.html', context)

def companyProfileView(request):

    company = Company.objects.get(user=request.user)

    context = {
        'company': company,
    }

    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.isProfilEdited == False:
            if request.user.role == 0:
                return redirect('/editStudentProfile')
            elif request.user.role == 1:
                return redirect('/editCompanyProfile')

    return render(request, 'companyProfile.html', context)


def yourCoursesView(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.user.role == 0:
            title = 'Kursy na które jesteś zapisany'

            student = Student.objects.get(user=request.user)
            courses_query = Course.objects.filter(students=student)

            context = {
                'title': title,
                'courses_query': courses_query,
            }
        elif request.user.role == 1:
            title = 'Kursy które oferujesz'

            company = Company.objects.get(user=request.user)
            courses_query = Course.objects.filter(company=company)

            context = {
                'title': title,
                'courses_query': courses_query,
            }


    return render(request, 'yourCourses.html', context)