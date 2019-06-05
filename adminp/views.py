from django.shortcuts import render
from django.template import Context
from django.db.models import Q
from users.models import *
from courses.models import *
from news.models import *
from .models import *
from django.http import HttpResponse, JsonResponse, Http404
from django.utils.timezone import now
from django.core.mail import send_mail

def checkPermissions(request):
	if not request.user.is_superuser:
		raise Http404
def msgNotify(request):
	checkPermissions(request)
	sid = request.GET.get('id')
	if not sid is None:
		obj = AdminMessage.objects.get(id=sid)
		obj.read = True
		obj.save()
	msgCount = AdminMessage.objects.filter(read=False).count()
	return HttpResponse(str(msgCount))	
def index(request):
	checkPermissions(request)
	msgCount = AdminMessage.objects.filter(read=False).count()
	
	context = {
		'messagesCount': msgCount,
		'admin_page': True,
	}
	return render(request, 'adminp_index.html', context)
def overviewList(request):
	checkPermissions(request)
	entries = []
	
	row = {}
	row['name'] = u'Liczba kursantów'
	row['value'] = Student.objects.all().count()
	entries.append(row)
	row = {}
	row['name'] = u'Liczba firm szkoleniowych'
	row['value'] = Company.objects.all().count()
	entries.append(row)
	row = {}
	row['name'] = u'Liczba administratorów'
	row['value'] = MyUser.objects.filter(is_superuser=True).count()
	entries.append(row)
	row = {}
	row['name'] = u'Liczba kursów'
	row['value'] = Course.objects.all().count()
	entries.append(row)
	row = {}
	row['name'] = u'Liczba komentarzy w kursach'
	row['value'] = CourseComment.objects.all().count()
	entries.append(row)
	row = {}
	row['name'] = u'Liczba newsów'
	row['value'] = Post.objects.all().count()
	entries.append(row)
	row = {}
	row['name'] = u'Liczba komentarzy w newsach'
	row['value'] = PostComment.objects.all().count()
	entries.append(row)
	
	
	context = {
		'entries': entries,
	}
	return render(request, 'adminp_overview_list.html', context)

###################################

def adminsAdd(request):
	checkPermissions(request)
	login = request.GET.get('login')
	if login is None:
		return HttpResponse('0')
	password = request.GET.get('password')
	if password is None:
		return HttpResponse('0')
	first_name = request.GET.get('first_name')
	if first_name is None:
		return HttpResponse('0')
	last_name = request.GET.get('last_name')
	if last_name is None:
		return HttpResponse('0')
	
	objList = MyUser()
	objList.username = login
	objList.email = login
	objList.set_password(password)
	objList.first_name = first_name
	objList.last_name = last_name
	objList.is_superuser = True
	objList.is_staff = True
	objList.is_active = True
	objList.role = 2
	objList.date_joined = now()
	objList.isProfilEdited = False
	objList.save()
	
	return HttpResponse('1')
	
def msgSendForm(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	objList = AdminMessage.objects.get(id = objId)
	emailX = request.user.email
	atIdx = emailX.find('@')
	adminEmail = emailX[:atIdx] + '@szkolup.pythonanywhere.com'
	context = {
		'entry': objList,
		'adminEmail': adminEmail,
	}
	return render(request, 'adminp_msg_send.html', context)
def msgSend(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	subject = request.GET.get('subject')
	if subject is None:
		return HttpResponse('0')
	content = request.GET.get('content')
	if content is None:
		return HttpResponse('0')
	
	obj = AdminMessage.objects.get(id = objId)
	
	
	emailX = request.user.email
	atIdx = emailX.find('@')
	adminEmail = emailX[:atIdx] + '@szkolup.pythonanywhere.com'
	
	

	# send_mail(
		# subject,
		# content,
		# adminEmail,
		# [obj.email],
		# fail_silently=False,
	# )
	
	print('Sending ' + adminEmail)
	print(subject)
	print(content)
	
	obj.delete()
	
	return HttpResponse('1')
###################################


def usersList(request):
	checkPermissions(request)
	pageNumber = request.GET.get('page')
	if pageNumber is None:
		pageNumber = 1
	displayCount = request.GET.get('display')
	if displayCount is None:
		displayCount = 1
	filterCategory = request.GET.get('filter')
	if filterCategory is None:
		filterCategory = 0
	searchPhrase = request.GET.get('search')
	if searchPhrase is None:
		searchPhrase = ''
	sortColumn = request.GET.get('sortcol')
	if sortColumn is None:
		sortColumn = 1
	sortOrder = request.GET.get('sortord')
	if sortOrder is None:
		sortOrder = 1
	
	pageNumber = int(pageNumber)
	displayCount = int(displayCount)
	filterCategory = int(filterCategory)
	sortColumn = int(sortColumn)
	sortOrder = int(sortOrder)
	
	countDict = {1: 10, 2: 25, 3: 50, 4: 100}
	
	sortDict = { 1: 'id', 2: 'email', 3: 'name', 4: 'surname', 5: 'city', 6: 'street', 7: 'house_number', 8: 'flat_number',  }
	if sortOrder == 1:
		sortString = ''
	else:
		sortString = '-'
	
	sortString += sortDict[sortColumn]
	
	displayCount = countDict[displayCount]
	
	entry_from = (pageNumber-1) * displayCount
	entry_to = entry_from + displayCount
	
	
	if searchPhrase != '':
		
		if filterCategory == 0:
			filterCategory = 0x7FFFFFFF
		
		
		queryFilter = Q(pk=None)
		
		if (filterCategory & 2) != 0:
			queryFilter |= Q(id__icontains=searchPhrase)
		
		elif (filterCategory & 4) != 0:
			queryFilter |= Q(email__icontains=searchPhrase)
		
		elif (filterCategory & 8) != 0:
			queryFilter |= Q(name__icontains=searchPhrase)
		
		elif (filterCategory & 16) != 0:
			queryFilter |= Q(surname__icontains=searchPhrase)
		
		elif (filterCategory & 32) != 0:
			queryFilter |= Q(city__icontains=searchPhrase)
		
		elif (filterCategory & 64) != 0:
			queryFilter |= Q(street__icontains=searchPhrase)
		
		elif (filterCategory & 128) != 0:
			queryFilter |= Q(house_number__icontains=searchPhrase)
		
		elif (filterCategory & 256) != 0:
			queryFilter |= Q(flat_number__icontains=searchPhrase)
		
		
		
		
		listObj = Student.objects.filter(queryFilter).order_by(sortString)
	else:
		
		listObj = Student.objects.all().order_by(sortString)
		
		
	
	allCount = listObj.count()
	objList = listObj[entry_from:entry_to]
	
	entry_to = min(entry_to, allCount)
	
	pageRadius = 4
	
	pageMax = int(allCount / displayCount) + 1
	pageLeft = pageNumber - pageRadius
	pageRight = pageNumber + pageRadius
	if pageLeft < 1:
		pageLeft = 1
	if pageRight > pageMax:
		pageRight = pageMax
	
	pages = []
	for p in range(pageLeft, pageRight + 1):
		pages.append(Context({'num': p, 'active': p == pageNumber}))
	
	if pageNumber <= 1:
		prevPage = None
	else:
		prevPage = pageNumber - 1
	if pageNumber >= pageMax:
		nextPage = None
	else:
		nextPage = pageNumber + 1
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	context = {
		'entries': objList,
		'pages': pages,
		'prev': prevPage,
		'next': nextPage,
		'count_from': entry_from + 1,
		'count_to': entry_to,
		'count_all': allCount,
		'sortCol': sortColumn,
		'sortOrd': sortOrder,
	}
	return render(request, 'adminp_users_list.html', context)

def usersEditForm(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		objId = 1
	objList = Student.objects.get(id = objId)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	context = {
		'entry': objList,
	}
	return render(request, 'adminp_users_edit.html', context)

def usersDelete(request):
	checkPermissions(request)
	#return HttpResponse('1') #test
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	objList = Student.objects.get(id = objId)
	objList.delete()
	return HttpResponse('1')

def usersUpdate(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	
	password = request.GET.get('password')
	if password is None:
		return HttpResponse('0')
	
	name = request.GET.get('name')
	if name is None:
		return HttpResponse('0')
	
	surname = request.GET.get('surname')
	if surname is None:
		return HttpResponse('0')
	
	city = request.GET.get('city')
	if city is None:
		return HttpResponse('0')
	
	street = request.GET.get('street')
	if street is None:
		return HttpResponse('0')
	
	house_number = request.GET.get('house_number')
	if house_number is None:
		return HttpResponse('0')
	
	flat_number = request.GET.get('flat_number')
	if flat_number is None:
		return HttpResponse('0')
	
	
	
	objList = Student.objects.get(id = objId)
	
	
	usr = objList.user
	if password != '':
		usr.set_password(password)
		usr.save()
	
	
	
	objList.name = name
	
	
	
	objList.surname = surname
	
	
	
	objList.city = city
	
	
	
	objList.street = street
	
	
	
	objList.house_number = house_number
	
	
	
	objList.flat_number = flat_number
	
	
	objList.save()
	
	return HttpResponse('1')










def companiesList(request):
	checkPermissions(request)
	pageNumber = request.GET.get('page')
	if pageNumber is None:
		pageNumber = 1
	displayCount = request.GET.get('display')
	if displayCount is None:
		displayCount = 1
	filterCategory = request.GET.get('filter')
	if filterCategory is None:
		filterCategory = 0
	searchPhrase = request.GET.get('search')
	if searchPhrase is None:
		searchPhrase = ''
	sortColumn = request.GET.get('sortcol')
	if sortColumn is None:
		sortColumn = 1
	sortOrder = request.GET.get('sortord')
	if sortOrder is None:
		sortOrder = 1
	
	pageNumber = int(pageNumber)
	displayCount = int(displayCount)
	filterCategory = int(filterCategory)
	sortColumn = int(sortColumn)
	sortOrder = int(sortOrder)
	
	countDict = {1: 10, 2: 25, 3: 50, 4: 100}
	
	sortDict = { 1: 'id', 2: 'email', 3: 'company_name', 4: 'city', 5: 'street', 6: 'house_number', 7: 'flat_number',  }
	if sortOrder == 1:
		sortString = ''
	else:
		sortString = '-'
	
	sortString += sortDict[sortColumn]
	
	displayCount = countDict[displayCount]
	
	entry_from = (pageNumber-1) * displayCount
	entry_to = entry_from + displayCount
	
	
	if searchPhrase != '':
		
		if filterCategory == 0:
			filterCategory = 0x7FFFFFFF
		
		
		queryFilter = Q(pk=None)
		
		if (filterCategory & 2) != 0:
			queryFilter |= Q(id__icontains=searchPhrase)
		
		elif (filterCategory & 4) != 0:
			queryFilter |= Q(email__icontains=searchPhrase)
		
		elif (filterCategory & 8) != 0:
			queryFilter |= Q(company_name__icontains=searchPhrase)
		
		elif (filterCategory & 16) != 0:
			queryFilter |= Q(city__icontains=searchPhrase)
		
		elif (filterCategory & 32) != 0:
			queryFilter |= Q(street__icontains=searchPhrase)
		
		elif (filterCategory & 64) != 0:
			queryFilter |= Q(house_number__icontains=searchPhrase)
		
		elif (filterCategory & 128) != 0:
			queryFilter |= Q(flat_number__icontains=searchPhrase)
		
		
		
		
		listObj = Company.objects.filter(queryFilter).order_by(sortString)
	else:
		
		listObj = Company.objects.all().order_by(sortString)
		
		
	
	allCount = listObj.count()
	objList = listObj[entry_from:entry_to]
	
	entry_to = min(entry_to, allCount)
	
	pageRadius = 4
	
	pageMax = int(allCount / displayCount) + 1
	pageLeft = pageNumber - pageRadius
	pageRight = pageNumber + pageRadius
	if pageLeft < 1:
		pageLeft = 1
	if pageRight > pageMax:
		pageRight = pageMax
	
	pages = []
	for p in range(pageLeft, pageRight + 1):
		pages.append(Context({'num': p, 'active': p == pageNumber}))
	
	if pageNumber <= 1:
		prevPage = None
	else:
		prevPage = pageNumber - 1
	if pageNumber >= pageMax:
		nextPage = None
	else:
		nextPage = pageNumber + 1
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	context = {
		'entries': objList,
		'pages': pages,
		'prev': prevPage,
		'next': nextPage,
		'count_from': entry_from + 1,
		'count_to': entry_to,
		'count_all': allCount,
		'sortCol': sortColumn,
		'sortOrd': sortOrder,
	}
	return render(request, 'adminp_companies_list.html', context)

def companiesEditForm(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		objId = 1
	objList = Company.objects.get(id = objId)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	context = {
		'entry': objList,
	}
	return render(request, 'adminp_companies_edit.html', context)

def companiesDelete(request):
	checkPermissions(request)
	#return HttpResponse('1') #test
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	objList = Company.objects.get(id = objId)
	objList.delete()
	return HttpResponse('1')

def companiesUpdate(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	
	password = request.GET.get('password')
	if password is None:
		return HttpResponse('0')
	
	company_name = request.GET.get('company_name')
	if company_name is None:
		return HttpResponse('0')
	
	city = request.GET.get('city')
	if city is None:
		return HttpResponse('0')
	
	street = request.GET.get('street')
	if street is None:
		return HttpResponse('0')
	
	house_number = request.GET.get('house_number')
	if house_number is None:
		return HttpResponse('0')
	
	flat_number = request.GET.get('flat_number')
	if flat_number is None:
		return HttpResponse('0')
	
	
	
	objList = Company.objects.get(id = objId)
	
	
	usr = objList.user
	if password != '':
		usr.set_password(password)
		usr.save()
	
	
	
	objList.company_name = company_name
	
	
	
	objList.city = city
	
	
	
	objList.street = street
	
	
	
	objList.house_number = house_number
	
	
	
	objList.flat_number = flat_number
	
	
	objList.save()
	
	return HttpResponse('1')










def adminsList(request):
	checkPermissions(request)
	pageNumber = request.GET.get('page')
	if pageNumber is None:
		pageNumber = 1
	displayCount = request.GET.get('display')
	if displayCount is None:
		displayCount = 1
	filterCategory = request.GET.get('filter')
	if filterCategory is None:
		filterCategory = 0
	searchPhrase = request.GET.get('search')
	if searchPhrase is None:
		searchPhrase = ''
	sortColumn = request.GET.get('sortcol')
	if sortColumn is None:
		sortColumn = 1
	sortOrder = request.GET.get('sortord')
	if sortOrder is None:
		sortOrder = 1
	
	pageNumber = int(pageNumber)
	displayCount = int(displayCount)
	filterCategory = int(filterCategory)
	sortColumn = int(sortColumn)
	sortOrder = int(sortOrder)
	
	countDict = {1: 10, 2: 25, 3: 50, 4: 100}
	
	sortDict = { 1: 'id', 2: 'email', 3: 'first_name', 4: 'last_name',  }
	if sortOrder == 1:
		sortString = ''
	else:
		sortString = '-'
	
	sortString += sortDict[sortColumn]
	
	displayCount = countDict[displayCount]
	
	entry_from = (pageNumber-1) * displayCount
	entry_to = entry_from + displayCount
	
	
	if searchPhrase != '':
		
		if filterCategory == 0:
			filterCategory = 0x7FFFFFFF
		
		
		queryFilter = Q(pk=None)
		
		if (filterCategory & 2) != 0:
			queryFilter |= Q(id__icontains=searchPhrase)
		
		elif (filterCategory & 4) != 0:
			queryFilter |= Q(email__icontains=searchPhrase)
		
		elif (filterCategory & 8) != 0:
			queryFilter |= Q(first_name__icontains=searchPhrase)
		
		elif (filterCategory & 16) != 0:
			queryFilter |= Q(last_name__icontains=searchPhrase)
		
		
		
		queryFilter &= Q(is_superuser=True)
		
		
		listObj = MyUser.objects.filter(queryFilter).order_by(sortString)
	else:
		
		listObj = MyUser.objects.filter(is_superuser=True).order_by(sortString)
		
		
	
	allCount = listObj.count()
	objList = listObj[entry_from:entry_to]
	
	entry_to = min(entry_to, allCount)
	
	pageRadius = 4
	
	pageMax = int(allCount / displayCount) + 1
	pageLeft = pageNumber - pageRadius
	pageRight = pageNumber + pageRadius
	if pageLeft < 1:
		pageLeft = 1
	if pageRight > pageMax:
		pageRight = pageMax
	
	pages = []
	for p in range(pageLeft, pageRight + 1):
		pages.append(Context({'num': p, 'active': p == pageNumber}))
	
	if pageNumber <= 1:
		prevPage = None
	else:
		prevPage = pageNumber - 1
	if pageNumber >= pageMax:
		nextPage = None
	else:
		nextPage = pageNumber + 1
	
	
	
	
	
	
	
	
	
	
	
	
	context = {
		'entries': objList,
		'pages': pages,
		'prev': prevPage,
		'next': nextPage,
		'count_from': entry_from + 1,
		'count_to': entry_to,
		'count_all': allCount,
		'sortCol': sortColumn,
		'sortOrd': sortOrder,
	}
	return render(request, 'adminp_admins_list.html', context)

def adminsEditForm(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		objId = 1
	objList = MyUser.objects.get(id = objId)
	
	
	
	
	
	
	
	
	
	context = {
		'entry': objList,
	}
	return render(request, 'adminp_admins_edit.html', context)

def adminsDelete(request):
	checkPermissions(request)
	#return HttpResponse('1') #test
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	objList = MyUser.objects.get(id = objId)
	objList.delete()
	return HttpResponse('1')

def adminsUpdate(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	
	password = request.GET.get('password')
	if password is None:
		return HttpResponse('0')
	
	first_name = request.GET.get('first_name')
	if first_name is None:
		return HttpResponse('0')
	
	last_name = request.GET.get('last_name')
	if last_name is None:
		return HttpResponse('0')
	
	
	
	objList = MyUser.objects.get(id = objId)
	
	
	usr = objList
	if password != '':
		usr.set_password(password)
		
	
	
	
	objList.first_name = first_name
	
	
	
	objList.last_name = last_name
	
	
	objList.save()
	
	return HttpResponse('1')










def coursesList(request):
	checkPermissions(request)
	pageNumber = request.GET.get('page')
	if pageNumber is None:
		pageNumber = 1
	displayCount = request.GET.get('display')
	if displayCount is None:
		displayCount = 1
	filterCategory = request.GET.get('filter')
	if filterCategory is None:
		filterCategory = 0
	searchPhrase = request.GET.get('search')
	if searchPhrase is None:
		searchPhrase = ''
	sortColumn = request.GET.get('sortcol')
	if sortColumn is None:
		sortColumn = 1
	sortOrder = request.GET.get('sortord')
	if sortOrder is None:
		sortOrder = 1
	
	pageNumber = int(pageNumber)
	displayCount = int(displayCount)
	filterCategory = int(filterCategory)
	sortColumn = int(sortColumn)
	sortOrder = int(sortOrder)
	
	countDict = {1: 10, 2: 25, 3: 50, 4: 100}
	
	sortDict = { 1: 'id', 2: 'title', 3: 'start_date', 5: 'price', 6: 'region', 7: 'city', 8: 'category', 9: 'subcategory', 10: 'max_students', 11: 'has_certificate', 12: 'views_count', 13: 'comment_count',  }
	if sortOrder == 1:
		sortString = ''
	else:
		sortString = '-'
	
	sortString += sortDict[sortColumn]
	
	displayCount = countDict[displayCount]
	
	entry_from = (pageNumber-1) * displayCount
	entry_to = entry_from + displayCount
	
	
	if searchPhrase != '':
		
		if filterCategory == 0:
			filterCategory = 0x7FFFFFFF
		
		
		queryFilter = Q(pk=None)
		
		if (filterCategory & 2) != 0:
			queryFilter |= Q(id__icontains=searchPhrase)
		
		elif (filterCategory & 4) != 0:
			queryFilter |= Q(title__icontains=searchPhrase)
		
		elif (filterCategory & 8) != 0:
			queryFilter |= Q(start_date__icontains=searchPhrase)
		
		elif (filterCategory & 32) != 0:
			queryFilter |= Q(price__icontains=searchPhrase)
		
		elif (filterCategory & 64) != 0:
			queryFilter |= Q(region__icontains=searchPhrase)
		
		elif (filterCategory & 128) != 0:
			queryFilter |= Q(city__icontains=searchPhrase)
		
		elif (filterCategory & 256) != 0:
			queryFilter |= Q(category__icontains=searchPhrase)
		
		elif (filterCategory & 512) != 0:
			queryFilter |= Q(subcategory__icontains=searchPhrase)
		
		elif (filterCategory & 1024) != 0:
			queryFilter |= Q(max_students__icontains=searchPhrase)
		
		elif (filterCategory & 2048) != 0:
			queryFilter |= Q(has_certificate__icontains=searchPhrase)
		
		elif (filterCategory & 4096) != 0:
			queryFilter |= Q(views_count__icontains=searchPhrase)
		
		elif (filterCategory & 8192) != 0:
			queryFilter |= Q(comment_count__icontains=searchPhrase)
		
		
		
		
		listObj = Course.objects.filter(queryFilter).order_by(sortString)
	else:
		
		listObj = Course.objects.all().order_by(sortString)
		
		
	
	allCount = listObj.count()
	objList = listObj[entry_from:entry_to]
	
	entry_to = min(entry_to, allCount)
	
	pageRadius = 4
	
	pageMax = int(allCount / displayCount) + 1
	pageLeft = pageNumber - pageRadius
	pageRight = pageNumber + pageRadius
	if pageLeft < 1:
		pageLeft = 1
	if pageRight > pageMax:
		pageRight = pageMax
	
	pages = []
	for p in range(pageLeft, pageRight + 1):
		pages.append(Context({'num': p, 'active': p == pageNumber}))
	
	if pageNumber <= 1:
		prevPage = None
	else:
		prevPage = pageNumber - 1
	if pageNumber >= pageMax:
		nextPage = None
	else:
		nextPage = pageNumber + 1
	
	
	
	
	
	
	
	
	
	for o in objList:
	
		o.start_date = o.start_date.strftime("%Y-%m-%d")
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	context = {
		'entries': objList,
		'pages': pages,
		'prev': prevPage,
		'next': nextPage,
		'count_from': entry_from + 1,
		'count_to': entry_to,
		'count_all': allCount,
		'sortCol': sortColumn,
		'sortOrd': sortOrder,
	}
	return render(request, 'adminp_courses_list.html', context)

def coursesEditForm(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		objId = 1
	objList = Course.objects.get(id = objId)
	
	
	
	
	
	
	objList.start_date = objList.start_date.strftime("%Y-%m-%d")
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	context = {
		'entry': objList,
	}
	return render(request, 'adminp_courses_edit.html', context)

def coursesDelete(request):
	checkPermissions(request)
	#return HttpResponse('1') #test
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	objList = Course.objects.get(id = objId)
	objList.delete()
	return HttpResponse('1')

def coursesUpdate(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	
	title = request.GET.get('title')
	if title is None:
		return HttpResponse('0')
	
	start_date = request.GET.get('start_date')
	if start_date is None:
		return HttpResponse('0')
	
	price = request.GET.get('price')
	if price is None:
		return HttpResponse('0')
	
	region = request.GET.get('region')
	if region is None:
		return HttpResponse('0')
	
	city = request.GET.get('city')
	if city is None:
		return HttpResponse('0')
	
	category = request.GET.get('category')
	if category is None:
		return HttpResponse('0')
	
	subcategory = request.GET.get('subcategory')
	if subcategory is None:
		return HttpResponse('0')
	
	max_students = request.GET.get('max_students')
	if max_students is None:
		return HttpResponse('0')
	
	has_certificate = request.GET.get('has_certificate')
	if has_certificate is None:
		return HttpResponse('0')
	
	
	
	objList = Course.objects.get(id = objId)
	
	
	objList.title = title
	
	
	
	objList.start_date = start_date
	
	
	
	objList.price = price
	
	
	
	objList.region = region
	
	
	
	objList.city = city
	
	
	
	objList.category = category
	
	
	
	objList.subcategory = subcategory
	
	
	
	objList.max_students = max_students
	
	
	
	objList.has_certificate = has_certificate
	
	
	objList.save()
	
	return HttpResponse('1')










def newsList(request):
	checkPermissions(request)
	pageNumber = request.GET.get('page')
	if pageNumber is None:
		pageNumber = 1
	displayCount = request.GET.get('display')
	if displayCount is None:
		displayCount = 1
	filterCategory = request.GET.get('filter')
	if filterCategory is None:
		filterCategory = 0
	searchPhrase = request.GET.get('search')
	if searchPhrase is None:
		searchPhrase = ''
	sortColumn = request.GET.get('sortcol')
	if sortColumn is None:
		sortColumn = 1
	sortOrder = request.GET.get('sortord')
	if sortOrder is None:
		sortOrder = 1
	
	pageNumber = int(pageNumber)
	displayCount = int(displayCount)
	filterCategory = int(filterCategory)
	sortColumn = int(sortColumn)
	sortOrder = int(sortOrder)
	
	countDict = {1: 10, 2: 25, 3: 50, 4: 100}
	
	sortDict = { 1: 'id', 2: 'title', 3: 'timestamp', 4: 'view_count', 5: 'comment_count', 6: 'featured',  }
	if sortOrder == 1:
		sortString = ''
	else:
		sortString = '-'
	
	sortString += sortDict[sortColumn]
	
	displayCount = countDict[displayCount]
	
	entry_from = (pageNumber-1) * displayCount
	entry_to = entry_from + displayCount
	
	
	if searchPhrase != '':
		
		if filterCategory == 0:
			filterCategory = 0x7FFFFFFF
		
		
		queryFilter = Q(pk=None)
		
		if (filterCategory & 2) != 0:
			queryFilter |= Q(id__icontains=searchPhrase)
		
		elif (filterCategory & 4) != 0:
			queryFilter |= Q(title__icontains=searchPhrase)
		
		elif (filterCategory & 8) != 0:
			queryFilter |= Q(timestamp__icontains=searchPhrase)
		
		elif (filterCategory & 16) != 0:
			queryFilter |= Q(view_count__icontains=searchPhrase)
		
		elif (filterCategory & 32) != 0:
			queryFilter |= Q(comment_count__icontains=searchPhrase)
		
		elif (filterCategory & 64) != 0:
			queryFilter |= Q(featured__icontains=searchPhrase)
		
		
		
		
		listObj = Post.objects.filter(queryFilter).order_by(sortString)
	else:
		
		listObj = Post.objects.all().order_by(sortString)
		
		
	
	allCount = listObj.count()
	objList = listObj[entry_from:entry_to]
	
	entry_to = min(entry_to, allCount)
	
	pageRadius = 4
	
	pageMax = int(allCount / displayCount) + 1
	pageLeft = pageNumber - pageRadius
	pageRight = pageNumber + pageRadius
	if pageLeft < 1:
		pageLeft = 1
	if pageRight > pageMax:
		pageRight = pageMax
	
	pages = []
	for p in range(pageLeft, pageRight + 1):
		pages.append(Context({'num': p, 'active': p == pageNumber}))
	
	if pageNumber <= 1:
		prevPage = None
	else:
		prevPage = pageNumber - 1
	if pageNumber >= pageMax:
		nextPage = None
	else:
		nextPage = pageNumber + 1
	
	
	
	
	
	
	
	
	
	for o in objList:
	
		o.timestamp = o.timestamp.strftime("%Y-%m-%d")
	
	
	
	
	
	
	
	
	
	
	context = {
		'entries': objList,
		'pages': pages,
		'prev': prevPage,
		'next': nextPage,
		'count_from': entry_from + 1,
		'count_to': entry_to,
		'count_all': allCount,
		'sortCol': sortColumn,
		'sortOrd': sortOrder,
	}
	return render(request, 'adminp_news_list.html', context)

def newsEditForm(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		objId = 1
	objList = Post.objects.get(id = objId)
	
	
	
	
	
	
	objList.timestamp = objList.timestamp.strftime("%Y-%m-%d")
	
	
	
	
	
	
	
	
	context = {
		'entry': objList,
	}
	return render(request, 'adminp_news_edit.html', context)

def newsDelete(request):
	checkPermissions(request)
	#return HttpResponse('1') #test
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	objList = Post.objects.get(id = objId)
	objList.delete()
	return HttpResponse('1')

def newsUpdate(request):
	checkPermissions(request)
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	
	title = request.GET.get('title')
	if title is None:
		return HttpResponse('0')
	
	timestamp = request.GET.get('timestamp')
	if timestamp is None:
		return HttpResponse('0')
	
	view_count = request.GET.get('view_count')
	if view_count is None:
		return HttpResponse('0')
	
	comment_count = request.GET.get('comment_count')
	if comment_count is None:
		return HttpResponse('0')
	
	featured = request.GET.get('featured')
	if featured is None:
		return HttpResponse('0')
	
	
	
	objList = Post.objects.get(id = objId)
	
	
	objList.title = title
	
	
	
	objList.timestamp = timestamp
	
	
	
	objList.view_count = view_count
	
	
	
	objList.comment_count = comment_count
	
	
	
	objList.featured = featured
	
	
	objList.save()
	
	return HttpResponse('1')










def msgList(request):
	checkPermissions(request)
	pageNumber = request.GET.get('page')
	if pageNumber is None:
		pageNumber = 1
	displayCount = request.GET.get('display')
	if displayCount is None:
		displayCount = 1
	filterCategory = request.GET.get('filter')
	if filterCategory is None:
		filterCategory = 0
	searchPhrase = request.GET.get('search')
	if searchPhrase is None:
		searchPhrase = ''
	sortColumn = request.GET.get('sortcol')
	if sortColumn is None:
		sortColumn = 1
	sortOrder = request.GET.get('sortord')
	if sortOrder is None:
		sortOrder = 1
	
	pageNumber = int(pageNumber)
	displayCount = int(displayCount)
	filterCategory = int(filterCategory)
	sortColumn = int(sortColumn)
	sortOrder = int(sortOrder)
	
	countDict = {1: 10, 2: 25, 3: 50, 4: 100}
	
	sortDict = { 1: 'name', 2: 'email', 3: 'content', 4: 'time',  }
	if sortOrder == 1:
		sortString = ''
	else:
		sortString = '-'
	
	sortString += sortDict[sortColumn]
	
	displayCount = countDict[displayCount]
	
	entry_from = (pageNumber-1) * displayCount
	entry_to = entry_from + displayCount
	
	
	if searchPhrase != '':
		
		if filterCategory == 0:
			filterCategory = 0x7FFFFFFF
		
		
		queryFilter = Q(pk=None)
		
		if (filterCategory & 2) != 0:
			queryFilter |= Q(name__icontains=searchPhrase)
		
		elif (filterCategory & 4) != 0:
			queryFilter |= Q(email__icontains=searchPhrase)
		
		elif (filterCategory & 8) != 0:
			queryFilter |= Q(content__icontains=searchPhrase)
		
		elif (filterCategory & 16) != 0:
			queryFilter |= Q(time__icontains=searchPhrase)
		
		
		
		
		listObj = AdminMessage.objects.filter(queryFilter).order_by(sortString)
	else:
		
		listObj = AdminMessage.objects.all().order_by(sortString)
		
		
	
	allCount = listObj.count()
	objList = listObj[entry_from:entry_to]
	
	entry_to = min(entry_to, allCount)
	
	pageRadius = 4
	
	pageMax = int(allCount / displayCount) + 1
	pageLeft = pageNumber - pageRadius
	pageRight = pageNumber + pageRadius
	if pageLeft < 1:
		pageLeft = 1
	if pageRight > pageMax:
		pageRight = pageMax
	
	pages = []
	for p in range(pageLeft, pageRight + 1):
		pages.append(Context({'num': p, 'active': p == pageNumber}))
	
	if pageNumber <= 1:
		prevPage = None
	else:
		prevPage = pageNumber - 1
	if pageNumber >= pageMax:
		nextPage = None
	else:
		nextPage = pageNumber + 1
	
	
	
	
	
	
	
	
	
	
	
	for o in objList:
	
		o.time = o.time.strftime("%Y-%m-%d")
	
	
	
	
	
	
	for o in objList:
	
		cont = o.content
		if len(cont) > 20:
			o.content = cont[:20] + '...'
	
	context = {
		'entries': objList,
		'pages': pages,
		'prev': prevPage,
		'next': nextPage,
		'count_from': entry_from + 1,
		'count_to': entry_to,
		'count_all': allCount,
		'sortCol': sortColumn,
		'sortOrd': sortOrder,
	}
	return render(request, 'adminp_msg_list.html', context)

def msgDelete(request):
	checkPermissions(request)
	#return HttpResponse('1') #test
	objId = request.GET.get('id')
	if objId is None:
		return HttpResponse('0')
	objList = AdminMessage.objects.get(id = objId)
	objList.delete()
	return HttpResponse('1')









