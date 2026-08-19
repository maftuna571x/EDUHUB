from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SettingsForm
from .models import User
from apps.school.models import (
    Group,
    Assignment,
    AssignmentSubmission,
    Grade,
)


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

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


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect("login")


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    user = request.user

    # =====================================================
    # STUDENT DASHBOARD
    # =====================================================

    if user.role == User.Role.STUDENT:

        student_groups = (
            user.student_groups
            .select_related(
                "subject",
                "classroom",
                "teacher",
            )
            .all()
        )

        assignments = (
            Assignment.objects
            .filter(
                group__students=user,
                is_active=True,
            )
            .select_related(
                "group",
                "group__subject",
                "group__classroom",
                "teacher",
            )
            .distinct()
            .order_by("due_date")
        )

        submissions = AssignmentSubmission.objects.filter(
            student=user
        )

        submitted_assignment_ids = set(
            submissions.values_list(
                "assignment_id",
                flat=True,
            )
        )

        total_assignments = assignments.count()

        submitted_count = (
            submissions
            .filter(
                assignment__in=assignments
            )
            .values("assignment")
            .distinct()
            .count()
        )

        if total_assignments > 0:

            progress = round(
                (submitted_count / total_assignments) * 100
            )

        else:

            progress = 0

        grades = Grade.objects.filter(
            student=user
        )

        grade_count = grades.count()

        if grade_count > 0:

            average_grade = round(
                sum(
                    grade.score
                    for grade in grades
                ) / grade_count,
                1,
            )

        else:

            average_grade = 0

        recent_assignments = assignments[:5]

        context = {
            "user": user,

            "student_groups": student_groups,

            "assignments": assignments,

            "recent_assignments": recent_assignments,

            "submitted_assignment_ids":
                submitted_assignment_ids,

            "total_assignments":
                total_assignments,

            "submitted_count":
                submitted_count,

            "progress":
                progress,

            "average_grade":
                average_grade,

            "grade_count":
                grade_count,
        }

        return render(
            request,
            "users/student_dashboard.html",
            context,
        )

    # =====================================================
    # TEACHER DASHBOARD
    # =====================================================

    if user.role == User.Role.TEACHER:

        # -------------------------------------------------
        # TEACHER'S GROUPS
        # -------------------------------------------------

        teaching_groups = (
            Group.objects
            .filter(
                teacher=user
            )
            .select_related(
                "subject",
                "classroom",
            )
            .prefetch_related(
                "students"
            )
            .order_by("name")
        )

        # -------------------------------------------------
        # TOTAL CLASSES
        # -------------------------------------------------

        total_classes = teaching_groups.count()

        # -------------------------------------------------
        # TEACHER'S STUDENTS
        # -------------------------------------------------

        teacher_students = (
            User.objects
            .filter(
                role=User.Role.STUDENT,
                student_groups__teacher=user,
            )
            .distinct()
            .order_by(
                "first_name",
                "last_name",
                "username",
            )
        )

        total_students = teacher_students.count()

        # -------------------------------------------------
        # TEACHER'S ASSIGNMENTS
        # -------------------------------------------------

        assignments = (
            Assignment.objects
            .filter(
                teacher=user,
                is_active=True,
            )
            .select_related(
                "group",
                "group__subject",
                "group__classroom",
            )
            .order_by("-due_date", "-id")
        )

        total_assignments = assignments.count()

        recent_assignments = assignments[:5]

        # -------------------------------------------------
        # CONTEXT
        # -------------------------------------------------

        context = {

            # Current user
            "user": user,

            # =============================================
            # CLASSES
            # =============================================

            "teaching_groups":
                teaching_groups,

            "teacher_groups":
                teaching_groups,

            "groups":
                teaching_groups,

            "total_classes":
                total_classes,

            "my_classes_count":
                total_classes,

            # =============================================
            # STUDENTS
            # =============================================

            "teacher_students":
                teacher_students,

            "students":
                teacher_students,

            "total_students":
                total_students,

            # =============================================
            # ASSIGNMENTS
            # =============================================

            "assignments":
                assignments,

            "teacher_assignments":
                assignments,

            "total_assignments":
                total_assignments,

            "recent_assignments":
                recent_assignments,
        }

        return render(
            request,
            "users/teacher_dashboard.html",
            context,
        )

    # =====================================================
    # ADMIN / OTHER ROLES
    # =====================================================

    return render(
        request,
        "users/dashboard.html",
        {
            "user": user,
        },
    )


# =========================================================
# ADMIN — STUDENTS
# =========================================================

@login_required
def admin_students(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    students = (
        User.objects
        .filter(
            role=User.Role.STUDENT
        )
        .order_by(
            "first_name",
            "last_name",
            "username",
        )
    )

    return render(
        request,
        "users/admin_students.html",
        {
            "students": students,
        },
    )


# =========================================================
# ADMIN — CREATE STUDENT
# =========================================================

@login_required
def admin_create_student(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            "",
        ).strip()

        last_name = request.POST.get(
            "last_name",
            "",
        ).strip()

        username = request.POST.get(
            "username",
            "",
        ).strip()

        email = request.POST.get(
            "email",
            "",
        ).strip()

        phone = request.POST.get(
            "phone",
            "",
        ).strip()

        password = request.POST.get(
            "password",
            "",
        )

        password_confirm = request.POST.get(
            "password_confirm",
            "",
        )

        context = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "phone": phone,
        }

        # ---------------------------------------------
        # USERNAME
        # ---------------------------------------------

        if not username:

            context["error"] = (
                "Username kiritish shart."
            )

            return render(
                request,
                "users/admin_create_student.html",
                context,
            )

        # ---------------------------------------------
        # PASSWORD
        # ---------------------------------------------

        if not password:

            context["error"] = (
                "Password kiritish shart."
            )

            return render(
                request,
                "users/admin_create_student.html",
                context,
            )

        # ---------------------------------------------
        # PASSWORD CONFIRM
        # ---------------------------------------------

        if password != password_confirm:

            context["error"] = (
                "Passwordlar bir xil emas."
            )

            return render(
                request,
                "users/admin_create_student.html",
                context,
            )

        # ---------------------------------------------
        # USERNAME EXISTS
        # ---------------------------------------------

        if User.objects.filter(
            username=username
        ).exists():

            context["error"] = (
                "Bu username allaqachon mavjud."
            )

            return render(
                request,
                "users/admin_create_student.html",
                context,
            )

        # ---------------------------------------------
        # EMAIL EXISTS
        # ---------------------------------------------

        if email and User.objects.filter(
            email=email
        ).exists():

            context["error"] = (
                "Bu email allaqachon mavjud."
            )

            return render(
                request,
                "users/admin_create_student.html",
                context,
            )

        # ---------------------------------------------
        # CREATE STUDENT
        # ---------------------------------------------

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=User.Role.STUDENT,
        )

        return redirect(
            "admin_students"
        )

    return render(
        request,
        "users/admin_create_student.html",
    )


# =========================================================
# SETTINGS
# =========================================================

@login_required
def settings_view(request):

    if request.method == "POST":

        form = SettingsForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "settings"
            )

    else:

        form = SettingsForm(
            instance=request.user,
        )

    return render(
        request,
        "users/settings.html",
        {
            "form": form,
        },
    )