from django.shortcuts import render, redirect, get_object_or_404, reverse
from courses.models import Category, Subcategory, Region, City, Course, CourseComment, CourseRate
from users.models import Student
from users.models import Company
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def addCourseView(request):

    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.role == 1:
            regions = Region.objects.order_by('name')
            cities = City.objects.order_by('name')
            categories = Category.objects.order_by('name')
            subcategories = Subcategory.objects.order_by('name')

            context = {
                'regions': regions,
                'cities': cities,
                'categories': categories,
                'subcategories': subcategories,
            }

            if request.method == 'POST':
                title = request.POST['title']

                try:
                    overview = request.POST['overview']
                except:
                    overview = ''

                start_date = request.POST['startDate']
                price = request.POST['price']
                region = request.POST['region']
                city = request.POST['city']
                category = request.POST['category']
                subcategory = request.POST['subcategory']
                max_students = request.POST['maxStudents']
                thumbnail = request.FILES['imageInput']

                try:
                    has_certificate = request.POST['hasCertificate']
                except:
                    has_certificate = ''

                if has_certificate == 'on':
                    certificate = True
                else:
                    certificate = False

                company = Company.objects.get(user=request.user)

                print(company)

                course = Course.objects.create(
                    title=title,
                    overview=overview,
                    start_date=start_date,
                    price=price,
                    region=region,
                    city=city,
                    category=category,
                    subcategory=subcategory,
                    max_students=max_students,
                    has_certificate=certificate,
                    thumbnail=thumbnail,
                    company=company,
                )

                course.save()
                return redirect('/')

            return render(request, 'addCourse.html', context)
        else:
            return redirect('/')
    return redirect('/')

def coursesView(request):

    courses = Course.objects.all()
    regions = Region.objects.order_by('name')
    cities = City.objects.order_by('name')
    categories = Category.objects.order_by('name')
    subcategories = Subcategory.objects.order_by('name')

    title = request.GET.get('title')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    minStartDate = request.GET.get('minStartDate')
    maxStartDate = request.GET.get('maxStartDate')
    region = request.GET.get('region')
    city = request.GET.get('city')
    certTrue = request.GET.get('certificateTrue')
    certFalse = request.GET.get('certificateFalse')

    if title != '' and title is not None:
        courses = courses.filter(Q(title__icontains=title))

    if category != '' and category is not None and category != 'Wybierz...':
        courses = courses.filter(category=category)

    if subcategory != '' and subcategory is not None and subcategory != 'Wybierz...':
        courses = courses.filter(subcategory=subcategory)

    if minPrice != '' and minPrice is not None:
        courses = courses.filter(price__gte=minPrice)

    if maxPrice != '' and maxPrice is not None:
        courses = courses.filter(price__lte=maxPrice)

    if minStartDate != '' and minStartDate is not None:
        courses = courses.filter(start_date__gte=minStartDate)

    if maxStartDate != '' and maxStartDate is not None:
        courses = courses.filter(start_date__lte=maxStartDate)

    if region != '' and region is not None and region != 'Wybierz...':
        courses = courses.filter(region=region)

    if city != '' and city is not None and city != 'Wybierz...':
        courses = courses.filter(city=city)

    if certTrue == 'on':
        courses = courses.filter(has_certificate=True)
    elif certFalse == 'on':
        courses = courses.filter(has_certificate=False)

    ### Paginacja

    paginator = Paginator(courses, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_courses = paginator.page(page)
    except PageNotAnInteger:
        paginated_courses = paginator.page(1)
    except EmptyPage:
        paginated_courses = paginator.page(paginator.num_pages)

    context = {
        'regions': regions,
        'cities': cities,
        'categories': categories,
        'subcategories': subcategories,
        'courses_list': paginated_courses,
        'page_request_var': page_request_var,
        'title': title,
        'category': category,
        'subcategory': subcategory,
        'maxPrice': maxPrice,
        'minPrice': minPrice,
        'minStartDate': minStartDate,
        'maxStartDate': maxStartDate,
        'region': region,
        'city': city,
        'certTrue': certTrue,
        'certFalse': certFalse,
    }

    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.isProfilEdited == False:
            if request.user.role == 0:
                return redirect('/editStudentProfile')
            elif request.user.role == 1:
                return redirect('/editCompanyProfile')

    return render(request, 'courses.html', context)



def courseDetailView(request, id):

    course = get_object_or_404(Course, id=id)

    students = Student.objects.filter(course=course)
    countStudents = students.count()

    if request.method == 'POST':
        if request.POST['submit'] == 'addComment':
            commentAuthorName = request.POST['username']
            commentAuthorEmail = request.POST['useremail']
            commentContent = request.POST['comment']

            newComment = CourseComment.objects.create(
                author_name=commentAuthorName,
                author_email=commentAuthorEmail,
                content=commentContent,
                course=course,
            )

            newComment.save()
            course.comment_count = course.comment_count + 1
            course.save()

    comments = CourseComment.objects.filter(course=course)


    # Ocena kursu
    sumRate = 0
    course_rates = CourseRate.objects.filter(course=course)

    if not course_rates:
        course_rate = '-'
    else:
        myCourse_rates = iter(course_rates)
        for i in myCourse_rates:
            sumRate += i.value

        course_rate = sumRate/course_rates.count()

    msg = ''

    if request.method == 'POST':
        if request.POST['submit'] == 'addRate':
            try:
                rate = request.POST['rate']
            except:
                rate = ''

            if rate == '' or rate is None:
                msg = ''
            else:
                rateExists = CourseRate.objects.filter(course=course, user=request.user)

                if rateExists:
                    msg = 'Już oceniłeś ten kurs'
                else:
                    rateObj = CourseRate.objects.create(
                        value=rate,
                        user=request.user,
                        course=course,
                    )

                    rateObj.save()
                    msg = 'Twoja ocena została zapisana.'

    context = {
        'current_course': course,
        'comments': comments,
        'countStudents': countStudents,
        'course_rate': course_rate,
        'msg': msg,
    }

    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.isProfilEdited == False:
            if request.user.role == 0:
                return redirect('/editStudentProfile')
            elif request.user.role == 1:
                return redirect('/editCompanyProfile')

    return render(request, 'course_detail.html', context)

def saveToCourseView(request, id):

    course = get_object_or_404(Course, id=id)
    student = Student.objects.get(user=request.user)

    if request.user.role != 0:
        msg = 'Brak możliwości zapisu na kurs.'
    else:
        course_students_list = list(course.students.all())

        if len(course_students_list) < course.max_students:
            if(course_students_list.__contains__(student)):
                msg = 'Jestes juz zapisany na ten kurs.'
            else:

                course.students.add(student)
                course.save()

                msg = 'Pomyslnie zapisano na kurs.'
        else:
            msg = 'Brak wolnych miejsc.'



    context = {
        'current_course': course,
        'msg': msg
    }

    return render(request, 'course_save.html', context)

def courseDelete(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect(reverse('userProfil'))