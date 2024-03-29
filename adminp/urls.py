"""KursyProjekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
	path('overviewList', overviewList),
	path('usersList', usersList),
	path('usersEditForm', usersEditForm),
	path('usersDelete', usersDelete),
	path('usersUpdate', usersUpdate),
	path('companiesList', companiesList),
	path('companiesEditForm', companiesEditForm),
	path('companiesDelete', companiesDelete),
	path('companiesUpdate', companiesUpdate),
	path('adminsList', adminsList),
	path('adminsEditForm', adminsEditForm),
	path('adminsDelete', adminsDelete),
	path('adminsUpdate', adminsUpdate),
	path('adminsAdd', adminsAdd),
	path('coursesList', coursesList),
	path('coursesEditForm', coursesEditForm),
	path('coursesDelete', coursesDelete),
	path('coursesUpdate', coursesUpdate),
	path('newsList', newsList),
	path('newsEditForm', newsEditForm),
	path('newsDelete', newsDelete),
	path('newsUpdate', newsUpdate),
	path('msgList', msgList),
	path('msgDelete', msgDelete),
	path('msgNotify', msgNotify),
	path('msgSendForm', msgSendForm),
	path('msgSend', msgSend),
]
