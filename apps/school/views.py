from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.users.models import User

from .models import (
    Assignment,
    AssignmentSubmission,
    Group,
)


@login_required
def create_assignment(request):
    if request.user.role != User.Role.TEACHER:
        return redirect("dashboard")

    groups = Group.objects.filter(
        teacher=request.user,
        is_active=True,
    )

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        group_id = request.POST.get("group")
        due_date = request.POST.get("due_date")

        group = get_object_or_404(
            Group,
            id=group_id,
            teacher=request.user,
            is_active=True,
        )

        Assignment.objects.create(
            title=title,
            description=description,
            group=group,
            teacher=request.user,
            due_date=due_date,
        )

        return redirect("teacher_assignments")

    return render(
        request,
        "school/create_assignment.html",
        {
            "groups": groups,
        },
    )


@login_required
def teacher_assignments(request):
    if request.user.role != User.Role.TEACHER:
        return redirect("dashboard")

    assignments = (
        Assignment.objects
        .filter(
            teacher=request.user,
            is_active=True,
        )
        .select_related(
            "group",
            "group__subject",
        )
    )

    return render(
        request,
        "school/teacher_assignments.html",
        {
            "assignments": assignments,
        },
    )


@login_required
def student_assignments(request):
    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    assignments = (
        Assignment.objects
        .filter(
            group__students=request.user,
            is_active=True,
        )
        .select_related(
            "group",
            "group__subject",
            "teacher",
        )
        .distinct()
    )

    return render(
        request,
        "school/student_assignments.html",
        {
            "assignments": assignments,
        },
    )


@login_required
def submit_assignment(request, assignment_id):
    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        is_active=True,
        group__students=request.user,
    )

    submission = (
        AssignmentSubmission.objects
        .filter(
            assignment=assignment,
            student=request.user,
        )
        .first()
    )

    submitted = False

    if request.method == "POST":
        answer = request.POST.get("answer", "").strip()

        submission, created = AssignmentSubmission.objects.update_or_create(
            assignment=assignment,
            student=request.user,
            defaults={
                "answer": answer,
                "submitted_at": timezone.now(),
            },
        )

        submitted = True

    return render(
        request,
        "school/submit_assignment.html",
        {
            "assignment": assignment,
            "submission": submission,
            "submitted": submitted,
        },
    )






@login_required
def assignment_submissions(request, assignment_id):
    if request.user.role != User.Role.TEACHER:
        return redirect("dashboard")

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        teacher=request.user,
        is_active=True,
    )

    submissions = (
        AssignmentSubmission.objects
        .filter(assignment=assignment)
        .select_related("student")
        .order_by("-submitted_at")
    )

    return render(
        request,
        "school/assignment_submissions.html",
        {
            "assignment": assignment,
            "submissions": submissions,
        },
    )