from django.contrib import admin

from .models import (
    Subject,
    Classroom,
    Group,
    Grade,
    Assignment,
    AssignmentSubmission,
    CommunityMessage,
    Vocabulary,
    VocabularyFavorite,
    VocabularyProgress,
    VocabularySet,
)

from apps.users.models import User


# =========================================================
# SUBJECT
# =========================================================

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


# =========================================================
# CLASSROOM
# =========================================================

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


# =========================================================
# GROUP
# =========================================================

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

    filter_horizontal = (
        "students",
    )

    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(
            request,
            obj,
            **kwargs,
        )

        if "teacher" in form.base_fields:
            form.base_fields["teacher"].queryset = User.objects.filter(
                role=User.Role.TEACHER
            )

        if "students" in form.base_fields:
            form.base_fields["students"].queryset = User.objects.filter(
                role=User.Role.STUDENT
            )

        return form


# =========================================================
# ASSIGNMENT
# =========================================================

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

        form = super().get_form(
            request,
            obj,
            **kwargs,
        )

        if "teacher" in form.base_fields:
            form.base_fields["teacher"].queryset = User.objects.filter(
                role=User.Role.TEACHER
            )

        return form


# =========================================================
# ASSIGNMENT SUBMISSION
# =========================================================

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

        form = super().get_form(
            request,
            obj,
            **kwargs,
        )

        if "student" in form.base_fields:
            form.base_fields["student"].queryset = User.objects.filter(
                role=User.Role.STUDENT
            )

        return form


# =========================================================
# GRADE
# =========================================================

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

        form = super().get_form(
            request,
            obj,
            **kwargs,
        )

        if "student" in form.base_fields:
            form.base_fields["student"].queryset = User.objects.filter(
                role=User.Role.STUDENT
            )

        if "teacher" in form.base_fields:
            form.base_fields["teacher"].queryset = User.objects.filter(
                role=User.Role.TEACHER
            )

        return form


# =========================================================
# COMMUNITY MESSAGE
# =========================================================

@admin.register(CommunityMessage)
class CommunityMessageAdmin(admin.ModelAdmin):

    list_display = (
        "sender",
        "content_preview",
        "created_at",
    )

    list_filter = (
        "created_at",
        "sender__role",
    )

    search_fields = (
        "sender__username",
        "sender__first_name",
        "sender__last_name",
        "content",
    )

    ordering = (
        "-created_at",
    )

    @admin.display(description="Message")
    def content_preview(self, obj):

        return obj.content[:80]


# =========================================================
# SELF STUDY — VOCABULARY SET
# =========================================================

@admin.register(VocabularySet)
class VocabularySetAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "owner",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
    )

    ordering = (
        "-created_at",
    )


# =========================================================
# SELF STUDY — VOCABULARY
# =========================================================

@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):

    list_display = (
        "word",
        "translation",
        "level",
        "category",
        "is_public",
        "is_active",
        "created_by",
        "created_at",
    )

    list_filter = (
        "level",
        "category",
        "is_public",
        "is_active",
    )

    search_fields = (
        "word",
        "translation",
        "definition",
        "synonyms",
        "example",
    )

    ordering = (
        "level",
        "word",
    )


# =========================================================
# VOCABULARY FAVORITE
# =========================================================

@admin.register(VocabularyFavorite)
class VocabularyFavoriteAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "vocabulary",
        "created_at",
    )

    search_fields = (
        "user__username",
        "vocabulary__word",
    )

    ordering = (
        "-created_at",
    )


# =========================================================
# VOCABULARY PROGRESS
# =========================================================

@admin.register(VocabularyProgress)
class VocabularyProgressAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "vocabulary",
        "is_learned",
        "updated_at",
    )

    list_filter = (
        "is_learned",
    )

    search_fields = (
        "user__username",
        "vocabulary__word",
    )

    ordering = (
        "-updated_at",
    )