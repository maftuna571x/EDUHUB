"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.school import views as school_views
from apps.users import views as user_views


urlpatterns = [

    # =========================================================
    # ADMIN
    # =========================================================

    path(
        "admin/",
        admin.site.urls,
    ),


    # =========================================================
    # AUTHENTICATION
    # =========================================================

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


    # =========================================================
    # MAIN DASHBOARD
    # =========================================================

    path(
        "",
        user_views.dashboard,
        name="dashboard",
    ),


    # =========================================================
    # TEACHER
    # =========================================================

    path(
        "teacher/dashboard/",
        school_views.teacher_dashboard,
        name="teacher_dashboard",
    ),

    path(
        "teacher/classes/",
        school_views.teacher_classes,
        name="teacher_classes",
    ),

    path(
        "teacher/students/",
        school_views.teacher_students,
        name="teacher_students",
    ),

    path(
        "teacher/assignments/",
        school_views.teacher_assignments,
        name="teacher_assignments",
    ),

    path(
        "teacher/assignments/create/",
        school_views.create_assignment,
        name="create_assignment",
    ),

    path(
        "teacher/assignments/<int:assignment_id>/submissions/",
        school_views.assignment_submissions,
        name="assignment_submissions",
    ),

    path(
        "teacher/grades/",
        school_views.teacher_grades,
        name="teacher_grades",
    ),

    path(
        "teacher/messages/",
        school_views.teacher_messages,
        name="teacher_messages",
    ),


    # =========================================================
    # STUDENT
    # =========================================================

    path(
        "student/courses/",
        school_views.student_courses,
        name="student_courses",
    ),

    path(
        "student/courses/<int:group_id>/",
        school_views.student_course_detail,
        name="student_course_detail",
    ),

    path(
        "student/classes/",
        school_views.student_classes,
        name="student_classes",
    ),

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
        "student/grades/",
        school_views.student_grades,
        name="student_grades",
    ),

    path(
        "student/messages/",
        school_views.student_messages,
        name="student_messages",
    ),


    # =========================================================
    # PRIVATE MESSAGES
    # =========================================================

    path(
        "messages/<int:message_id>/read/",
        school_views.read_message,
        name="read_message",
    ),


    # =========================================================
    # NOTIFICATIONS
    # =========================================================

    path(
        "notifications/",
        school_views.notification_data,
        name="notification_data",
    ),


    # =========================================================
    # SETTINGS
    # =========================================================

    path(
        "settings/",
        user_views.settings_view,
        name="settings",
    ),


    # =========================================================
    # COMMUNITY
    # =========================================================

    path(
        "community/",
        school_views.community,
        name="community",
    ),

    path(
        "community/send/",
        school_views.community_send_message,
        name="community_send_message",
    ),

    path(
        "community/messages/",
        school_views.community_messages_api,
        name="community_messages_api",
    ),

    path(
        "community/notifications/<int:notification_id>/read/",
        school_views.read_community_notification,
        name="read_community_notification",
    ),


    # =========================================================
    # SELF STUDY — VOCABULARY
    # =========================================================

    path(
        "self-study/vocabulary/",
        school_views.vocabulary,
        name="vocabulary",
    ),

    # Create Set
    path(
        "self-study/vocabulary/sets/create/",
        school_views.vocabulary_set_create,
        name="vocabulary_set_create",
    ),

    # All Sets
    path(
        "self-study/vocabulary/sets/",
        school_views.vocabulary_sets,
        name="vocabulary_sets",
    ),

    # Set Detail
    path(
        "self-study/vocabulary/sets/<int:set_id>/",
        school_views.vocabulary_set_detail,
        name="vocabulary_set_detail",
    ),

    # Add Word to Set
    path(
        "self-study/vocabulary/sets/<int:set_id>/add/",
        school_views.vocabulary_set_add_word,
        name="vocabulary_add",
    ),

    # Remove Word from Set
    path(
        "self-study/vocabulary/sets/<int:set_id>/remove/<int:vocabulary_id>/",
        school_views.vocabulary_set_remove_word,
        name="vocabulary_set_remove_word",
    ),

    # Delete Set
    path(
        "self-study/vocabulary/sets/<int:set_id>/delete/",
        school_views.vocabulary_set_delete,
        name="vocabulary_set_delete",
    ),

    # Favorite
    path(
        "self-study/vocabulary/<int:vocabulary_id>/favorite/",
        school_views.vocabulary_favorite,
        name="vocabulary_favorite",
    ),

    # Learned
    path(
        "self-study/vocabulary/<int:vocabulary_id>/learned/",
        school_views.vocabulary_learned,
        name="vocabulary_learned",
    ),
    path(
        "self-study/vocabulary/sets/<int:set_id>/delete/",
        school_views.vocabulary_set_delete,
        name="vocabulary_set_delete",
    ),
    path(
        "student/grammar/",
        school_views.grammar_checker,
        name="grammar_checker",
    ),
    path(
        "reading/",
        school_views.reading_practice,
        name="reading_practice",
    ),
    path(
        "reading/<int:passage_id>/submit/",
        school_views.reading_submit,
        name="reading_submit",
    ),
    path(
        "reading/<int:passage_id>/test/",
        school_views.reading_test,
        name="reading_test",
    ),
    # =========================================================
    # LISTENING
    # =========================================================

    path(
        "listening/",
        school_views.listening_practice,
        name="listening_practice",
    ),
    path(
        "speaking/test/",
        school_views.speaking_test,
        name="speaking_test",
    ),
    path(
        "vocabulary-quiz/",
        school_views.vocabulary_quiz,
        name="vocabulary_quiz",
    ),
]


# =============================================================
# MEDIA FILES
# =============================================================

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
