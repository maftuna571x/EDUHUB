from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import User
from apps.school.models import Group, Assignment


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
                "error": "Username yoki password noto'g'ri.",
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

    if request.user.role == User.Role.STUDENT:
        return render(
            request,
            "users/student_dashboard.html",
        )

    if request.user.role == User.Role.TEACHER:
        return render(
            request,
            "users/teacher_dashboard.html",
        )

    if request.user.role == User.Role.ADMIN:

        total_students = User.objects.filter(
            role=User.Role.STUDENT
        ).count()

        total_teachers = User.objects.filter(
            role=User.Role.TEACHER
        ).count()

        total_groups = Group.objects.count()

        total_assignments = Assignment.objects.count()

        return render(
            request,
            "users/admin_dashboard.html",
            {
                "total_students": total_students,
                "total_teachers": total_teachers,
                "total_groups": total_groups,
                "total_assignments": total_assignments,
            },
        )

    if request.user.role == User.Role.STAFF:
        return render(
            request,
            "users/dashboard.html",
        )

    return redirect("login")



@login_required
def admin_students(request):
    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    students = (
        User.objects
        .filter(role=User.Role.STUDENT)
        .order_by("first_name", "last_name", "username")
    )

    return render(
        request,
        "users/admin_students.html",
        {
            "students": students,
        },
    )




@login_required
def admin_create_student(request):
    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    if request.method == "POST":

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        context = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "phone": phone,
        }

        if not username:
            context["error"] = "Username kiritish shart."
            return render(
                request,
                "users/admin_create_student.html",
                context,
            )

        if not password:
            context["error"] = "Password kiritish shart."
            return render(
                request,
                "users/admin_create_student.html",
                context,
            )

        if password != password_confirm:
            context["error"] = "Passwordlar bir xil emas."
            return render(
                request,
                "users/admin_create_student.html",
                context,
            )

        if User.objects.filter(username=username).exists():
            context["error"] = "Bu username allaqachon mavjud."
            return render(
                request,
                "users/admin_create_student.html",
                context,
            )

        if email and User.objects.filter(email=email).exists():
            context["error"] = "Bu email allaqachon mavjud."
            return render(
                request,
                "users/admin_create_student.html",
                context,
            )

        student = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=User.Role.STUDENT,
        )

        return redirect("admin_students")

    return render(
        request,
        "users/admin_create_student.html",
    )