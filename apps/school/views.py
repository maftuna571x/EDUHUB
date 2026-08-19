from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import JsonResponse
from django.db import models
from django.db.models import Q
from apps.users.models import User
import requests
from .models import (
    Assignment,
    AssignmentSubmission,
    Grade,
    Group,
    Message,
    CommunityMessage,
    CommunityNotification,
    VocabularyFavorite,
    VocabularyProgress,
    Vocabulary,
    VocabularySet,
)


# =========================================================
# ASSIGNMENTS
# =========================================================

@login_required
def create_assignment(request):

    if request.user.role != User.Role.TEACHER:
        return redirect("dashboard")

    groups = (
        Group.objects
        .filter(
            teacher=request.user,
            is_active=True,
        )
        .select_related(
            "subject",
            "classroom",
        )
        .prefetch_related(
            "students",
        )
        .order_by("name")
    )

    if request.method == "POST":

        title = request.POST.get(
            "title",
            "",
        ).strip()

        description = request.POST.get(
            "description",
            "",
        ).strip()

        group_id = request.POST.get(
            "group",
        )

        due_date = request.POST.get(
            "due_date",
        )

        if not title or not group_id:
            return render(
                request,
                "school/create_assignment.html",
                {
                    "groups": groups,
                    "error": "Title and group are required.",
                    "title": title,
                    "description": description,
                    "due_date": due_date,
                },
            )

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
        .order_by("-created_at")
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
        .order_by("due_date")
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

        answer = request.POST.get(
            "answer",
            "",
        ).strip()

        link = request.POST.get(
            "link",
            "",
        ).strip()

        uploaded_file = request.FILES.get(
            "file",
        )

        submission, created = (
            AssignmentSubmission.objects.update_or_create(
                assignment=assignment,
                student=request.user,
                defaults={
                    "answer": answer,
                    "link": link,
                    "submitted_at": timezone.now(),
                },
            )
        )

        if uploaded_file:
            submission.file = uploaded_file
            submission.save(
                update_fields=["file"]
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
        .filter(
            assignment=assignment,
        )
        .select_related(
            "student",
        )
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


# =========================================================
# GRADES
# =========================================================

@login_required
def student_grades(request):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    grades = (
        Grade.objects
        .filter(
            student=request.user,
        )
        .select_related(
            "subject",
            "assignment",
            "teacher",
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "school/student_grades.html",
        {
            "grades": grades,
        },
    )


@login_required
def teacher_grades(request):

    if request.user.role != User.Role.TEACHER:
        return redirect("dashboard")

    grades = (
        Grade.objects
        .filter(
            teacher=request.user,
        )
        .select_related(
            "student",
            "subject",
            "assignment",
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "school/teacher_grades.html",
        {
            "grades": grades,
        },
    )


# =========================================================
# TEACHER CLASSES
# =========================================================

@login_required
def teacher_classes(request):

    if request.user.role != User.Role.TEACHER:
        return redirect("dashboard")

    groups = (
        Group.objects
        .filter(
            teacher=request.user,
            is_active=True,
        )
        .select_related(
            "subject",
            "classroom",
        )
        .prefetch_related(
            "students",
        )
        .order_by("name")
    )

    return render(
        request,
        "school/teacher_classes.html",
        {
            "groups": groups,
        },
    )


# =========================================================
# TEACHER DASHBOARD
# =========================================================

@login_required
def teacher_dashboard(request):

    if request.user.role != User.Role.TEACHER:
        return redirect("dashboard")

    groups = (
        Group.objects
        .filter(
            teacher=request.user,
            is_active=True,
        )
        .select_related(
            "subject",
            "classroom",
        )
        .prefetch_related(
            "students",
        )
    )

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
        .order_by("-created_at")[:5]
    )

    total_students = sum(
        group.students.count()
        for group in groups
    )

    total_assignments = (
        Assignment.objects
        .filter(
            teacher=request.user,
            is_active=True,
        )
        .count()
    )

    unread_messages_count = (
        Message.objects
        .filter(
            receiver=request.user,
            is_read=False,
        )
        .count()
    )

    return render(
        request,
        "users/teacher_dashboard.html",
        {
            "groups": groups,
            "assignments": assignments,
            "total_groups": groups.count(),
            "total_students": total_students,
            "total_assignments": total_assignments,
            "unread_messages_count": unread_messages_count,
        },
    )


# =========================================================
# TEACHER STUDENTS
# =========================================================

@login_required
def teacher_students(request):

    if request.user.role != User.Role.TEACHER:
        return redirect("dashboard")

    groups = (
        Group.objects
        .filter(
            teacher=request.user,
            is_active=True,
        )
        .prefetch_related(
            "students",
        )
        .order_by("name")
    )

    students = (
        User.objects
        .filter(
            student_groups__teacher=request.user,
            student_groups__is_active=True,
            role=User.Role.STUDENT,
        )
        .distinct()
        .order_by(
            "first_name",
            "last_name",
            "username",
        )
    )

    return render(
        request,
        "school/teacher_students.html",
        {
            "students": students,
            "groups": groups,
        },
    )


# =========================================================
# STUDENT MESSAGES
# =========================================================

@login_required
def student_messages(request):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    teachers = (
        User.objects
        .filter(
            teaching_groups__students=request.user,
            role=User.Role.TEACHER,
        )
        .distinct()
        .order_by(
            "first_name",
            "last_name",
            "username",
        )
    )

    if request.method == "POST":

        receiver_id = request.POST.get(
            "receiver",
        )

        content = request.POST.get(
            "content",
            "",
        ).strip()

        teacher = get_object_or_404(
            User,
            id=receiver_id,
            role=User.Role.TEACHER,
            teaching_groups__students=request.user,
        )

        if content:

            Message.objects.create(
                sender=request.user,
                receiver=teacher,
                content=content,
            )

        return redirect("student_messages")

    sent_messages = (
        Message.objects
        .filter(
            sender=request.user,
        )
        .select_related(
            "receiver",
        )
        .order_by("-created_at")
    )

    received_messages = (
        Message.objects
        .filter(
            receiver=request.user,
        )
        .select_related(
            "sender",
        )
        .order_by("-created_at")
    )

    unread_count = (
        Message.objects
        .filter(
            receiver=request.user,
            is_read=False,
        )
        .count()
    )

    return render(
        request,
        "school/student_messages.html",
        {
            "teachers": teachers,
            "messages": sent_messages,
            "sent_messages": sent_messages,
            "received_messages": received_messages,
            "unread_count": unread_count,
        },
    )


# =========================================================
# TEACHER MESSAGES
# =========================================================

@login_required
def teacher_messages(request):

    if request.user.role != User.Role.TEACHER:
        return redirect("dashboard")

    students = (
        User.objects
        .filter(
            student_groups__teacher=request.user,
            role=User.Role.STUDENT,
        )
        .distinct()
        .order_by(
            "first_name",
            "last_name",
            "username",
        )
    )

    if request.method == "POST":

        receiver_id = request.POST.get(
            "receiver",
        )

        content = request.POST.get(
            "content",
            "",
        ).strip()

        student = get_object_or_404(
            User,
            id=receiver_id,
            role=User.Role.STUDENT,
            student_groups__teacher=request.user,
        )

        if content:

            Message.objects.create(
                sender=request.user,
                receiver=student,
                content=content,
            )

        return redirect("teacher_messages")

    received_messages = (
        Message.objects
        .filter(
            receiver=request.user,
        )
        .select_related(
            "sender",
        )
        .order_by("-created_at")
    )

    sent_messages = (
        Message.objects
        .filter(
            sender=request.user,
        )
        .select_related(
            "receiver",
        )
        .order_by("-created_at")
    )

    unread_count = (
        Message.objects
        .filter(
            receiver=request.user,
            is_read=False,
        )
        .count()
    )

    return render(
        request,
        "school/teacher_messages.html",
        {
            "students": students,
            "messages": received_messages,
            "sent_messages": sent_messages,
            "received_messages": received_messages,
            "unread_count": unread_count,
        },
    )


# =========================================================
# READ MESSAGE
# =========================================================

@login_required
def read_message(request, message_id):

    message = get_object_or_404(
        Message,
        id=message_id,
        receiver=request.user,
    )

    if not message.is_read:

        message.is_read = True

        message.save(
            update_fields=["is_read"]
        )

    if request.user.role == User.Role.TEACHER:
        return redirect("teacher_messages")

    if request.user.role == User.Role.STUDENT:
        return redirect("student_messages")

    return redirect("dashboard")


# =========================================================
# NOTIFICATIONS
# =========================================================

@login_required
def notification_data(request):

    if request.user.role not in [
        User.Role.STUDENT,
        User.Role.TEACHER,
    ]:
        return JsonResponse(
            {
                "count": 0,
                "messages": [],
            }
        )

    if not request.user.notifications_enabled:

        return JsonResponse(
            {
                "count": 0,
                "messages": [],
            }
        )

    data = []

    private_messages = (
        Message.objects
        .filter(
            receiver=request.user,
            is_read=False,
        )
        .select_related(
            "sender",
        )
        .order_by("-created_at")
    )

    for message in private_messages:

        sender_name = (
            message.sender.get_full_name().strip()
            or message.sender.username
        )

        data.append(
            {
                "id": message.id,
                "type": "message",
                "sender": sender_name,
                "content": message.content,
                "created_at": message.created_at.strftime(
                    "%b %d, %Y · %H:%M"
                ),
                "url": f"/messages/{message.id}/read/",
            }
        )

    community_notifications = (
        CommunityNotification.objects
        .filter(
            user=request.user,
            is_read=False,
        )
        .select_related(
            "message",
            "message__sender",
        )
        .order_by("-created_at")
    )

    for notification in community_notifications:

        community_message = notification.message

        sender_name = (
            community_message.sender.get_full_name().strip()
            or community_message.sender.username
        )

        data.append(
            {
                "id": notification.id,
                "type": "community",
                "sender": sender_name,
                "content": community_message.content,
                "created_at": notification.created_at.strftime(
                    "%b %d, %Y · %H:%M"
                ),
                "url": (
                    f"/community/notifications/"
                    f"{notification.id}/read/"
                ),
            }
        )

    data.sort(
        key=lambda item: item["created_at"],
        reverse=True,
    )

    return JsonResponse(
        {
            "count": len(data),
            "messages": data,
        }
    )


# =========================================================
# READ COMMUNITY NOTIFICATION
# =========================================================

@login_required
def read_community_notification(
    request,
    notification_id,
):

    notification = get_object_or_404(
        CommunityNotification,
        id=notification_id,
        user=request.user,
    )

    if not notification.is_read:

        notification.is_read = True

        notification.save(
            update_fields=["is_read"]
        )

    return redirect("community")


# =========================================================
# STUDENT COURSES
# =========================================================

@login_required
def student_courses(request):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    groups = (
        Group.objects
        .filter(
            students=request.user,
            is_active=True,
        )
        .select_related(
            "subject",
            "classroom",
            "teacher",
        )
        .order_by("name")
    )

    courses = []

    for group in groups:

        assignments = (
            Assignment.objects
            .filter(
                group=group,
                is_active=True,
            )
        )

        total_assignments = assignments.count()

        submitted_assignment_ids = set(
            AssignmentSubmission.objects
            .filter(
                assignment__in=assignments,
                student=request.user,
            )
            .values_list(
                "assignment_id",
                flat=True,
            )
        )

        completed_assignments = len(
            submitted_assignment_ids
        )

        if total_assignments > 0:

            progress = round(
                (
                    completed_assignments
                    / total_assignments
                ) * 100
            )

        else:

            progress = 0

        grades = (
            Grade.objects
            .filter(
                student=request.user,
                subject=group.subject,
                assignment__group=group,
            )
        )

        grade_values = list(
            grades.values_list(
                "score",
                flat=True,
            )
        )

        if grade_values:

            average_grade = round(
                sum(grade_values)
                / len(grade_values),
                1,
            )

        else:

            average_grade = None

        courses.append(
            {
                "group": group,
                "total_assignments": total_assignments,
                "completed_assignments": completed_assignments,
                "progress": progress,
                "average_grade": average_grade,
            }
        )

    return render(
        request,
        "school/student_courses.html",
        {
            "courses": courses,
        },
    )


@login_required
def student_course_detail(request, group_id):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    group = get_object_or_404(
        Group.objects.select_related(
            "subject",
            "classroom",
            "teacher",
        ),
        id=group_id,
        students=request.user,
        is_active=True,
    )

    assignments = list(
        Assignment.objects
        .filter(
            group=group,
            is_active=True,
        )
        .select_related(
            "teacher",
            "group",
            "group__subject",
        )
        .order_by("due_date")
    )

    submitted_assignment_ids = set(
        AssignmentSubmission.objects
        .filter(
            assignment__in=assignments,
            student=request.user,
        )
        .values_list(
            "assignment_id",
            flat=True,
        )
    )

    total_assignments = len(assignments)

    completed_assignments = len(
        submitted_assignment_ids
    )

    if total_assignments > 0:

        progress = round(
            (
                completed_assignments
                / total_assignments
            ) * 100
        )

    else:

        progress = 0

    grades = list(
        Grade.objects
        .filter(
            student=request.user,
            subject=group.subject,
            assignment__group=group,
        )
        .select_related(
            "teacher",
            "subject",
            "assignment",
        )
        .order_by("-created_at")
    )

    if grades:

        average_grade = round(
            sum(
                grade.score
                for grade in grades
            ) / len(grades),
            1,
        )

    else:

        average_grade = None

    return render(
        request,
        "school/student_course_detail.html",
        {
            "group": group,
            "assignments": assignments,
            "grades": grades,
            "submissions": submitted_assignment_ids,
            "total_assignments": total_assignments,
            "completed_assignments": completed_assignments,
            "progress": progress,
            "average_grade": average_grade,
        },
    )


# =========================================================
# STUDENT CLASSES
# =========================================================

@login_required
def student_classes(request):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    classes = (
        Group.objects
        .filter(
            students=request.user,
            is_active=True,
        )
        .select_related(
            "subject",
            "teacher",
            "classroom",
        )
        .order_by("name")
    )

    return render(
        request,
        "school/student_classes.html",
        {
            "classes": classes,
        },
    )


# =========================================================
# COMMUNITY
# =========================================================

@login_required
def community(request):

    if request.user.role not in [
        User.Role.STUDENT,
        User.Role.TEACHER,
    ]:
        return redirect("dashboard")

    messages = (
        CommunityMessage.objects
        .select_related(
            "sender",
        )
        .all()
        .order_by("created_at")
    )

    members = (
        User.objects
        .filter(
            role__in=[
                User.Role.STUDENT,
                User.Role.TEACHER,
            ]
        )
        .prefetch_related(
            "student_groups",
            "teaching_groups",
        )
        .order_by(
            "role",
            "first_name",
            "last_name",
            "username",
        )
    )

    return render(
        request,
        "school/community.html",
        {
            "community_messages": messages,
            "community_members": members,
        },
    )


# =========================================================
# COMMUNITY SEND MESSAGE
# =========================================================

@login_required
def community_send_message(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "error": "POST request required.",
            },
            status=405,
        )

    if request.user.role not in [
        User.Role.STUDENT,
        User.Role.TEACHER,
    ]:

        return JsonResponse(
            {
                "success": False,
                "error": "You are not allowed to send messages.",
            },
            status=403,
        )

    content = request.POST.get(
        "content",
        "",
    ).strip()

    if not content:

        return JsonResponse(
            {
                "success": False,
                "error": "Message cannot be empty.",
            },
            status=400,
        )

    if len(content) > 2000:

        return JsonResponse(
            {
                "success": False,
                "error": "Message is too long.",
            },
            status=400,
        )

    message = CommunityMessage.objects.create(
        sender=request.user,
        content=content,
    )

    recipients = (
        User.objects
        .filter(
            role__in=[
                User.Role.STUDENT,
                User.Role.TEACHER,
            ],
            notifications_enabled=True,
        )
        .exclude(
            id=request.user.id,
        )
    )

    CommunityNotification.objects.bulk_create(
        [
            CommunityNotification(
                user=user,
                message=message,
            )
            for user in recipients
        ],
        ignore_conflicts=True,
    )

    sender_name = (
        request.user.get_full_name().strip()
        or request.user.username
    )

    avatar_url = ""

    if getattr(request.user, "avatar", None):

        try:
            avatar_url = request.user.avatar.url
        except ValueError:
            avatar_url = ""

    return JsonResponse(
        {
            "success": True,
            "message": {
                "id": message.id,
                "sender_id": request.user.id,
                "sender_name": sender_name,
                "username": request.user.username,
                "role": request.user.role,
                "content": message.content,
                "created_at": message.created_at.strftime(
                    "%b %d, %Y · %H:%M"
                ),
                "avatar": avatar_url,
                "initial": sender_name[0].upper(),
            },
        }
    )


# =========================================================
# COMMUNITY MESSAGES API
# =========================================================

@login_required
def community_messages_api(request):

    if request.user.role not in [
        User.Role.STUDENT,
        User.Role.TEACHER,
    ]:

        return JsonResponse(
            {
                "success": False,
            },
            status=403,
        )

    messages = (
        CommunityMessage.objects
        .select_related(
            "sender",
        )
        .all()
        .order_by("created_at")
    )

    data = []

    for message in messages:

        sender_name = (
            message.sender.get_full_name().strip()
            or message.sender.username
        )

        avatar_url = ""

        if getattr(
            message.sender,
            "avatar",
            None,
        ):

            try:
                avatar_url = message.sender.avatar.url
            except ValueError:
                avatar_url = ""

        data.append(
            {
                "id": message.id,
                "sender_id": message.sender.id,
                "sender_name": sender_name,
                "username": message.sender.username,
                "role": message.sender.role,
                "content": message.content,
                "created_at": message.created_at.strftime(
                    "%b %d, %Y · %H:%M"
                ),
                "avatar": avatar_url,
                "initial": sender_name[0].upper(),
            }
        )

    return JsonResponse(
        {
            "success": True,
            "messages": data,
        }
    )


# =========================================================
# SELF STUDY — VOCABULARY
# =========================================================

@login_required
def vocabulary(request):

    if request.user.role not in [
        User.Role.STUDENT,
        User.Role.TEACHER,
    ]:
        return redirect("dashboard")

    search_query = request.GET.get(
        "q",
        "",
    ).strip()

    selected_level = request.GET.get(
        "level",
        "",
    ).strip()

    selected_category = request.GET.get(
        "category",
        "",
    ).strip()

    # -----------------------------------------------------
    # AVAILABLE VOCABULARY
    # Public words + user's own private words
    # -----------------------------------------------------

    vocabularies = (
        Vocabulary.objects
        .filter(
            is_active=True,
        )
        .filter(
            models.Q(is_public=True)
            |
            models.Q(created_by=request.user)
        )
        .select_related(
            "created_by",
        )
        .order_by(
            "word",
        )
    )

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if search_query:

        vocabularies = vocabularies.filter(
            models.Q(
                word__icontains=search_query
            )
            |
            models.Q(
                translation__icontains=search_query
            )
            |
            models.Q(
                definition__icontains=search_query
            )
            |
            models.Q(
                pronunciation__icontains=search_query
            )
            |
            models.Q(
                example__icontains=search_query
            )
            |
            models.Q(
                synonyms__icontains=search_query
            )
        )

    # -----------------------------------------------------
    # LEVEL
    # -----------------------------------------------------

    if selected_level:

        vocabularies = vocabularies.filter(
            level=selected_level,
        )

    # -----------------------------------------------------
    # CATEGORY
    # -----------------------------------------------------

    if selected_category:

        vocabularies = vocabularies.filter(
            category=selected_category,
        )

    # -----------------------------------------------------
    # FAVORITES
    # -----------------------------------------------------

    favorite_ids = set(
        VocabularyFavorite.objects
        .filter(
            user=request.user,
        )
        .values_list(
            "vocabulary_id",
            flat=True,
        )
    )

    # -----------------------------------------------------
    # LEARNED
    # -----------------------------------------------------

    learned_ids = set(
        VocabularyProgress.objects
        .filter(
            user=request.user,
            is_learned=True,
        )
        .values_list(
            "vocabulary_id",
            flat=True,
        )
    )

    # -----------------------------------------------------
    # TOTAL WORDS
    # -----------------------------------------------------

    visible_words = (
        Vocabulary.objects
        .filter(
            is_active=True,
        )
        .filter(
            models.Q(is_public=True)
            |
            models.Q(created_by=request.user)
        )
    )

    total_words = visible_words.count()

    # -----------------------------------------------------
    # LEARNED COUNT
    # -----------------------------------------------------

    learned_count = (
        VocabularyProgress.objects
        .filter(
            user=request.user,
            vocabulary__is_active=True,
            is_learned=True,
        )
        .filter(
            models.Q(
                vocabulary__is_public=True
            )
            |
            models.Q(
                vocabulary__created_by=request.user
            )
        )
        .count()
    )

    if total_words > 0:

        progress = round(
            (
                learned_count
                / total_words
            ) * 100
        )

    else:

        progress = 0

    # -----------------------------------------------------
    # CATEGORIES
    # -----------------------------------------------------

    categories = (
        Vocabulary.objects
        .filter(
            is_active=True,
        )
        .filter(
            models.Q(is_public=True)
            |
            models.Q(created_by=request.user)
        )
        .exclude(
            category="",
        )
        .values_list(
            "category",
            flat=True,
        )
        .distinct()
        .order_by(
            "category",
        )
    )

    # -----------------------------------------------------
    # LEVELS
    # -----------------------------------------------------

    levels = [
        "A1",
        "A2",
        "B1",
        "B2",
        "C1",
        "C2",
    ]

    # -----------------------------------------------------
    # USER'S SETS
    # -----------------------------------------------------

    vocabulary_sets = (
        VocabularySet.objects
        .filter(
            owner=request.user,
        )
        .prefetch_related(
            "words",
        )
        .order_by(
            "-created_at",
        )
    )

    return render(
        request,
        "school/vocabulary.html",
        {
            "vocabularies": vocabularies,
            "favorite_ids": favorite_ids,
            "learned_ids": learned_ids,
            "total_words": total_words,
            "learned_count": learned_count,
            "progress": progress,
            "categories": categories,
            "levels": levels,
            "search_query": search_query,
            "selected_level": selected_level,
            "selected_category": selected_category,
            "vocabulary_sets": vocabulary_sets,
        },
    )


# =========================================================
# VOCABULARY SETS
# =========================================================

@login_required
def vocabulary_sets(request):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    sets = (
        VocabularySet.objects
        .filter(
            owner=request.user,
        )
        .prefetch_related(
            "words",
        )
        .order_by(
            "-created_at",
        )
    )

    return render(
        request,
        "school/vocabulary_sets.html",
        {
            "sets": sets,
        },
    )


# =========================================================
# CREATE VOCABULARY SET
# =========================================================

@login_required
def vocabulary_set_create(request):

    if request.user.role != User.Role.STUDENT:
        return redirect("vocabulary")

    if request.method == "POST":

        name = request.POST.get(
            "name",
            "",
        ).strip()

        description = request.POST.get(
            "description",
            "",
        ).strip()

        if not name:

            return render(
                request,
                "school/vocabulary_set_create.html",
                {
                    "error": "Set name is required.",
                    "name": name,
                    "description": description,
                },
            )

        vocabulary_set = VocabularySet.objects.create(
            owner=request.user,
            name=name,
            description=description,
        )

        return redirect(
            "vocabulary_set_detail",
            set_id=vocabulary_set.id,
        )

    return render(
        request,
        "school/vocabulary_set_create.html",
    )







# =========================================================
# VOCABULARY SET DETAIL
# =========================================================





# =========================================================
# DELETE VOCABULARY SET
# =========================================================

@login_required
def vocabulary_set_delete(request, set_id):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    vocabulary_set = get_object_or_404(
        VocabularySet,
        id=set_id,
        owner=request.user,
    )

    if request.method == "POST":

        vocabulary_set.delete()

        return redirect("vocabulary_sets")

    return render(
        request,
        "school/vocabulary_set_delete.html",
        {
            "vocabulary_set": vocabulary_set,
        },
    )








@login_required
def vocabulary_set_detail(request, set_id):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    vocabulary_set = get_object_or_404(
        VocabularySet,
        id=set_id,
        owner=request.user,
    )

    words = vocabulary_set.words.filter(
        is_active=True,
    ).order_by("word")

    search_query = request.GET.get("q", "").strip()

    if search_query:
        words = words.filter(
            Q(word__icontains=search_query)
            | Q(translation__icontains=search_query)
            | Q(definition__icontains=search_query)
        )

    favorite_ids = set(
        VocabularyFavorite.objects.filter(
            user=request.user,
            vocabulary__in=words,
        ).values_list(
            "vocabulary_id",
            flat=True,
        )
    )

    learned_ids = set(
        VocabularyProgress.objects.filter(
            user=request.user,
            vocabulary__in=words,
            is_learned=True,
        ).values_list(
            "vocabulary_id",
            flat=True,
        )
    )

    return render(
        request,
        "school/vocabulary_set_detail.html",
        {
            "vocabulary_set": vocabulary_set,
            "words": words,
            "search_query": search_query,
            "favorite_ids": favorite_ids,
            "learned_ids": learned_ids,
        },
    )






# =========================================================
# ADD WORD TO SET
# =========================================================





@login_required
def vocabulary_set_add_word(request, set_id):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    vocabulary_set = get_object_or_404(
        VocabularySet,
        id=set_id,
        owner=request.user,
    )

    levels = [
        "A1",
        "A2",
        "B1",
        "B2",
        "C1",
        "C2",
    ]

    if request.method == "POST":

        word = request.POST.get("word", "").strip()
        translation = request.POST.get("translation", "").strip()
        definition = request.POST.get("definition", "").strip()
        pronunciation = request.POST.get("pronunciation", "").strip()
        example = request.POST.get("example", "").strip()
        synonyms = request.POST.get("synonyms", "").strip()
        level = request.POST.get("level", "B1").strip().upper()
        category = request.POST.get("category", "").strip()

        form_data = {
            "word": word,
            "translation": translation,
            "definition": definition,
            "pronunciation": pronunciation,
            "example": example,
            "synonyms": synonyms,
            "level": level,
            "category": category,
        }

        if level not in levels:
            level = "B1"
            form_data["level"] = level

        # REQUIRED FIELDS

        if not word:
            return render(
                request,
                "school/vocabulary_set_add_word.html",
                {
                    "vocabulary_set": vocabulary_set,
                    "levels": levels,
                    "error": "Word is required.",
                    **form_data,
                },
            )

        if not translation:
            return render(
                request,
                "school/vocabulary_set_add_word.html",
                {
                    "vocabulary_set": vocabulary_set,
                    "levels": levels,
                    "error": "Uzbek translation is required.",
                    **form_data,
                },
            )

        if not definition:
            return render(
                request,
                "school/vocabulary_set_add_word.html",
                {
                    "vocabulary_set": vocabulary_set,
                    "levels": levels,
                    "error": "Definition is required.",
                    **form_data,
                },
            )

        # FIND EXISTING WORD

        existing_word = (
            Vocabulary.objects
            .filter(
                word__iexact=word,
                is_active=True,
            )
            .filter(
                models.Q(is_public=True)
                | models.Q(created_by=request.user)
            )
            .first()
        )

        # USE EXISTING WORD

        if existing_word:

            vocabulary_item = existing_word

        # CREATE NEW WORD

        else:

            vocabulary_item = Vocabulary.objects.create(
                word=word,
                translation=translation,
                definition=definition,
                pronunciation=pronunciation,
                example=example,
                synonyms=synonyms,
                level=level,
                category=category,
                created_by=request.user,
                is_public=False,
                is_active=True,
            )

        # IMPORTANT:
        # ADD THIS WORD TO THIS SPECIFIC SET

        vocabulary_set.words.add(vocabulary_item)

        # GO BACK TO THE SAME SET

        return redirect(
            "vocabulary_set_detail",
            set_id=vocabulary_set.id,
        )

    return render(
        request,
        "school/vocabulary_set_add_word.html",
        {
            "vocabulary_set": vocabulary_set,
            "levels": levels,
        },
    )










# =========================================================
# REMOVE WORD FROM SET
# =========================================================

@login_required
def vocabulary_set_remove_word(
    request,
    set_id,
    vocabulary_id,
):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    vocabulary_set = get_object_or_404(
        VocabularySet,
        id=set_id,
        owner=request.user,
    )

    vocabulary_item = get_object_or_404(
        Vocabulary,
        id=vocabulary_id,
        is_active=True,
    )

    vocabulary_set.words.remove(
        vocabulary_item,
    )

    return redirect(
        "vocabulary_set_detail",
        set_id=vocabulary_set.id,
    )


# =========================================================
# DELETE VOCABULARY SET
# =========================================================

@login_required
def vocabulary_set_delete(
    request,
    set_id,
):

    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    vocabulary_set = get_object_or_404(
        VocabularySet,
        id=set_id,
        owner=request.user,
    )

    if request.method == "POST":

        vocabulary_set.delete()

        return redirect(
            "vocabulary_sets",
        )

    return render(
        request,
        "school/vocabulary_set_delete.html",
        {
            "vocabulary_set": vocabulary_set,
        },
    )


# =========================================================
# VOCABULARY ADD COMPATIBILITY
# =========================================================









# =========================================================
# VOCABULARY FAVORITE
# =========================================================

@login_required
def vocabulary_favorite(
    request,
    vocabulary_id,
):

    if request.user.role not in [
        User.Role.STUDENT,
        User.Role.TEACHER,
    ]:
        return redirect("dashboard")

    vocabulary_item = get_object_or_404(
        Vocabulary,
        id=vocabulary_id,
        is_active=True,
    )

    if (
        not vocabulary_item.is_public
        and vocabulary_item.created_by != request.user
    ):
        return redirect("vocabulary")

    favorite = (
        VocabularyFavorite.objects
        .filter(
            user=request.user,
            vocabulary=vocabulary_item,
        )
        .first()
    )

    if favorite:

        favorite.delete()

    else:

        VocabularyFavorite.objects.create(
            user=request.user,
            vocabulary=vocabulary_item,
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "vocabulary",
        )
    )


# =========================================================
# VOCABULARY LEARNED
# =========================================================

@login_required
def vocabulary_learned(
    request,
    vocabulary_id,
):

    if request.user.role not in [
        User.Role.STUDENT,
        User.Role.TEACHER,
    ]:
        return redirect("dashboard")

    vocabulary_item = get_object_or_404(
        Vocabulary,
        id=vocabulary_id,
        is_active=True,
    )

    if (
        not vocabulary_item.is_public
        and vocabulary_item.created_by != request.user
    ):
        return redirect("vocabulary")

    progress, created = (
        VocabularyProgress.objects
        .get_or_create(
            user=request.user,
            vocabulary=vocabulary_item,
        )
    )

    progress.is_learned = not progress.is_learned

    progress.save(
        update_fields=["is_learned"]
    )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "vocabulary",
        )
    )





@login_required
def grammar_checker(request):
    if request.user.role != User.Role.STUDENT:
        return redirect("dashboard")

    questions = [
        {
            "id": 1,
            "level": "A1",
            "topic": "Present Simple",
            "question": "She ___ to school every day.",
            "options": ["go", "goes", "going", "gone"],
            "answer": "goes",
            "explanation": "With he, she, and it, we usually add -s or -es to the verb in the Present Simple."
        },
        {
            "id": 2,
            "level": "A1",
            "topic": "Present Simple",
            "question": "I ___ English every evening.",
            "options": ["study", "studies", "studying", "studied"],
            "answer": "study",
            "explanation": "With I, we use the base form of the verb: study."
        },
        {
            "id": 3,
            "level": "A1",
            "topic": "To Be",
            "question": "They ___ students.",
            "options": ["am", "is", "are", "be"],
            "answer": "are",
            "explanation": "We use 'are' with they, we, and you."
        },
        {
            "id": 4,
            "level": "A1",
            "topic": "Past Simple",
            "question": "Yesterday, I ___ football.",
            "options": ["play", "plays", "played", "playing"],
            "answer": "played",
            "explanation": "The word 'yesterday' indicates the Past Simple. The past form of play is played."
        },
        {
            "id": 5,
            "level": "A1",
            "topic": "Articles",
            "question": "I have ___ apple.",
            "options": ["a", "an", "the", "no article"],
            "answer": "an",
            "explanation": "We use 'an' before words that begin with a vowel sound."
        },

        {
            "id": 6,
            "level": "A2",
            "topic": "Present Continuous",
            "question": "Look! The children ___ in the garden.",
            "options": ["play", "plays", "are playing", "played"],
            "answer": "are playing",
            "explanation": "We use Present Continuous for an action happening now."
        },
        {
            "id": 7,
            "level": "A2",
            "topic": "Comparatives",
            "question": "This book is ___ than that one.",
            "options": ["interesting", "more interesting", "most interesting", "interest"],
            "answer": "more interesting",
            "explanation": "For longer adjectives such as interesting, we use 'more' for the comparative."
        },
        {
            "id": 8,
            "level": "A2",
            "topic": "Modal Verbs",
            "question": "You ___ wear a seatbelt in a car.",
            "options": ["should", "can to", "must to", "are"],
            "answer": "should",
            "explanation": "'Should' is used to give advice or say what is a good idea."
        },
        {
            "id": 9,
            "level": "A2",
            "topic": "Prepositions",
            "question": "My birthday is ___ July.",
            "options": ["at", "on", "in", "from"],
            "answer": "in",
            "explanation": "We use 'in' with months: in July, in August, in December."
        },
        {
            "id": 10,
            "level": "A2",
            "topic": "Present Perfect",
            "question": "I have ___ this movie before.",
            "options": ["see", "saw", "seen", "seeing"],
            "answer": "seen",
            "explanation": "Present Perfect uses have/has + past participle. The past participle of see is seen."
        },

        {
            "id": 11,
            "level": "B1",
            "topic": "Present Perfect",
            "question": "She ___ in London since 2020.",
            "options": ["lives", "lived", "has lived", "is living"],
            "answer": "has lived",
            "explanation": "We use Present Perfect with 'since' when an action started in the past and continues until now."
        },
        {
            "id": 12,
            "level": "B1",
            "topic": "First Conditional",
            "question": "If it rains, we ___ at home.",
            "options": ["stay", "will stay", "stayed", "would stay"],
            "answer": "will stay",
            "explanation": "First Conditional uses: If + Present Simple, will + base verb."
        },
        {
            "id": 13,
            "level": "B1",
            "topic": "Passive Voice",
            "question": "English ___ in many countries.",
            "options": ["speaks", "is spoken", "spoke", "speaking"],
            "answer": "is spoken",
            "explanation": "This is Present Simple Passive: subject + is/are + past participle."
        },
        {
            "id": 14,
            "level": "B1",
            "topic": "Reported Speech",
            "question": "He said that he ___ tired.",
            "options": ["is", "was", "will", "has"],
            "answer": "was",
            "explanation": "In reported speech, present forms often change into past forms."
        },
        {
            "id": 15,
            "level": "B1",
            "topic": "Gerunds",
            "question": "I enjoy ___ English.",
            "options": ["learn", "to learn", "learning", "learned"],
            "answer": "learning",
            "explanation": "After 'enjoy', we normally use a gerund (-ing form)."
        },

        {
            "id": 16,
            "level": "B2",
            "topic": "Second Conditional",
            "question": "If I had more time, I ___ another language.",
            "options": ["learn", "will learn", "would learn", "learned"],
            "answer": "would learn",
            "explanation": "Second Conditional uses: If + Past Simple, would + base verb."
        },
        {
            "id": 17,
            "level": "B2",
            "topic": "Third Conditional",
            "question": "If I had studied harder, I ___ the exam.",
            "options": ["pass", "will pass", "would have passed", "passed"],
            "answer": "would have passed",
            "explanation": "Third Conditional talks about an unreal past situation: If + had + past participle, would have + past participle."
        },
        {
            "id": 18,
            "level": "B2",
            "topic": "Modal Perfect",
            "question": "You ___ have told me earlier.",
            "options": ["should", "should have", "must", "can"],
            "answer": "should have",
            "explanation": "'Should have + past participle' expresses criticism or regret about a past action."
        },
        {
            "id": 19,
            "level": "B2",
            "topic": "Relative Clauses",
            "question": "The woman ___ lives next door is a doctor.",
            "options": ["which", "where", "who", "when"],
            "answer": "who",
            "explanation": "We use 'who' for people in relative clauses."
        },
        {
            "id": 20,
            "level": "B2",
            "topic": "Inversion",
            "question": "Never ___ such a beautiful place.",
            "options": ["I have seen", "have I seen", "I saw", "saw I"],
            "answer": "have I seen",
            "explanation": "After negative adverbs such as 'never', formal English can use inversion: Never have I seen..."
        },

        {
            "id": 21,
            "level": "C1",
            "topic": "Mixed Conditionals",
            "question": "If I had taken that job, I ___ in London now.",
            "options": ["would live", "will live", "lived", "would have lived"],
            "answer": "would live",
            "explanation": "This is a mixed conditional: a past condition with a present result."
        },
        {
            "id": 22,
            "level": "C1",
            "topic": "Advanced Passive",
            "question": "The project is believed ___ successful.",
            "options": ["be", "to be", "being", "been"],
            "answer": "to be",
            "explanation": "After 'is believed', we commonly use the infinitive: is believed to be."
        },
        {
            "id": 23,
            "level": "C1",
            "topic": "Inversion",
            "question": "Rarely ___ such dedication from a student.",
            "options": ["we see", "do we see", "we saw", "see we"],
            "answer": "do we see",
            "explanation": "Negative or restrictive adverbs such as 'rarely' can trigger subject-auxiliary inversion."
        },
        {
            "id": 24,
            "level": "C1",
            "topic": "Participle Clauses",
            "question": "___ the instructions carefully, she completed the task.",
            "options": ["Reading", "Read", "Reads", "To reading"],
            "answer": "Reading",
            "explanation": "A present participle clause can describe an action happening at the same time."
        },
        {
            "id": 25,
            "level": "C1",
            "topic": "Advanced Modal Verbs",
            "question": "He ___ have forgotten about the meeting.",
            "options": ["must", "must have", "should", "can"],
            "answer": "must have",
            "explanation": "'Must have + past participle' expresses a strong deduction about the past."
        },
    ]

    selected_level = request.GET.get("level", "A1")
    selected_topic = request.GET.get("topic", "all")

    valid_levels = ["A1", "A2", "B1", "B2", "C1"]

    if selected_level not in valid_levels:
        selected_level = "A1"

    filtered_questions = [
        q for q in questions
        if q["level"] == selected_level
    ]

    if selected_topic != "all":
        filtered_questions = [
            q for q in filtered_questions
            if q["topic"] == selected_topic
        ]

    topics = sorted(
        {
            q["topic"]
            for q in questions
            if q["level"] == selected_level
        }
    )

    return render(
        request,
        "school/grammar_checker.html",
        {
            "questions": filtered_questions,
            "selected_level": selected_level,
            "selected_topic": selected_topic,
            "topics": topics,
            "levels": valid_levels,
        },
    )


