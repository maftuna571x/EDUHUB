from django.contrib import admin

from .models import (
    Subject,
    Classroom,
    Group,
    Grade,
    Assignment,
    AssignmentSubmission,
)

from apps.users.models import User


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )

    ordering = (
        "name",
    )


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "room_number",
        "capacity",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "room_number",
    )

    ordering = (
        "room_number",
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "teacher",
        "subject",
        "classroom",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "subject",
        "classroom",
    )

    search_fields = (
        "name",
        "teacher__username",
        "teacher__first_name",
        "teacher__last_name",
        "subject__name",
        "classroom__name",
        "classroom__room_number",
        "students__username",
        "students__first_name",
        "students__last_name",
    )

    ordering = (
        "name",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields["teacher"].queryset = User.objects.filter(
            role=User.Role.TEACHER
        )

        form.base_fields["students"].queryset = User.objects.filter(
            role=User.Role.STUDENT
        )

        return form


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "group",
        "teacher",
        "due_date",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "group",
        "teacher",
        "due_date",
    )

    search_fields = (
        "title",
        "description",
        "group__name",
        "teacher__username",
        "teacher__first_name",
        "teacher__last_name",
    )

    ordering = (
        "-created_at",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields["teacher"].queryset = User.objects.filter(
            role=User.Role.TEACHER
        )

        return form


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "assignment",
        "student",
        "submitted_at",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "assignment",
        "student",
        "submitted_at",
    )

    search_fields = (
        "assignment__title",
        "student__username",
        "student__first_name",
        "student__last_name",
    )

    ordering = (
        "-created_at",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields["student"].queryset = User.objects.filter(
            role=User.Role.STUDENT
        )

        return form


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "teacher",
        "assignment",
        "subject",
        "score",
        "created_at",
    )

    list_filter = (
        "assignment",
        "subject",
        "score",
        "created_at",
    )

    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
        "teacher__username",
        "teacher__first_name",
        "teacher__last_name",
        "subject__name",
        "assignment__title",
    )

    ordering = (
        "-created_at",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields["student"].queryset = User.objects.filter(
            role=User.Role.STUDENT
        )

        form.base_fields["teacher"].queryset = User.objects.filter(
            role=User.Role.TEACHER
        )

        return form