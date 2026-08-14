from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "users/login.html",
            {
                "error": "Username yoki password noto‘g‘ri.",
            },
        )

    return render(
        request,
        "users/login.html",
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    if request.user.role == User.Role.TEACHER:
        return render(
            request,
            "users/teacher_dashboard.html",
        )

    if request.user.role == User.Role.STUDENT:
        return render(
            request,
            "users/student_dashboard.html",
        )

    return render(
        request,
        "users/dashboard.html",
    )