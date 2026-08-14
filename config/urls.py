"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

from apps.school import views as school_views
from apps.users import views as user_views


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "login/",
        user_views.login_view,
        name="login",
    ),

    path(
        "logout/",
        user_views.logout_view,
        name="logout",
    ),

    path(
        "",
        user_views.dashboard,
        name="dashboard",
    ),

    # Teacher
    path(
        "teacher/assignments/create/",
        school_views.create_assignment,
        name="create_assignment",
    ),

    path(
        "teacher/assignments/",
        school_views.teacher_assignments,
        name="teacher_assignments",
    ),

    # Student
    path(
        "student/assignments/",
        school_views.student_assignments,
        name="student_assignments",
    ),

    path(
        "student/assignments/<int:assignment_id>/submit/",
        school_views.submit_assignment,
        name="submit_assignment",
    ),
    path(
        "teacher/assignments/<int:assignment_id>/submissions/",
        school_views.assignment_submissions,
        name="assignment_submissions",
    ),
]