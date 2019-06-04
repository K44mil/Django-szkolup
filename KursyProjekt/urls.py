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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from news.views import index, news, post, searchPostResult, post_delete, post_update, post_create
from .views import register
from users.views import registerStudent, registerCompany, loginView, logoutView,\
    userProfilView, editStudentProfileView, editCompanyProfileView, studentProfileView, companyProfileView,\
    yourCoursesView
from courses.views import addCourseView, coursesView, courseDetailView, saveToCourseView, courseDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('login/', loginView),
    path('news/', news, name='news'),
    path('create/', post_create, name = 'post-create'),
    path('post/<id>/', post, name = 'post-detail'),
    path('post/<id>/update/', post_update, name = 'post-update'),
    path('post/<id>/delete/', post_delete, name = 'post-delete'),
    path('searchPostResult/', searchPostResult, name='searchPostResult'),
    path('courses/', coursesView),
    path('register/', register),
    path('tinymce/', include('tinymce.urls')),
    path('registerStudent/', registerStudent),
    path('registerCompany/', registerCompany),
    path('userProfil/', userProfilView, name='userProfil'),
    path('logout/', logoutView),
    path('editStudentProfile/', editStudentProfileView),
    path('editCompanyProfile/', editCompanyProfileView),
    path('studentProfile/', studentProfileView),
    path('companyProfile/', companyProfileView),
    path('addCourse/', addCourseView),
    path('course_details/<id>/', courseDetailView, name="course-details"),
    path('course_save/<id>/', saveToCourseView, name="course-save"),
    path('course_details/<id>/delete', courseDelete, name='course-delete'),
    path('yourCourses/', yourCoursesView),
	path('adminp/', include('adminp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
