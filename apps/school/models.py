from django.db import models
from apps.users.models import User


# =========================================================
# SUBJECT
# =========================================================

class Subject(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


# =========================================================
# CLASSROOM
# =========================================================

class Classroom(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    room_number = models.CharField(
        max_length=20,
        unique=True,
    )

    capacity = models.PositiveIntegerField(
        default=20,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("room_number",)

    def __str__(self):
        return f"{self.name} ({self.room_number})"


# =========================================================
# GROUP
# =========================================================

class Group(models.Model):

    name = models.CharField(
        max_length=50,
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teaching_groups",
    )

    students = models.ManyToManyField(
        User,
        related_name="student_groups",
        blank=True,
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="groups",
    )

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.PROTECT,
        related_name="groups",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


# =========================================================
# ASSIGNMENT
# =========================================================

class Assignment(models.Model):

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    due_date = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


# =========================================================
# ASSIGNMENT SUBMISSION
# =========================================================

class AssignmentSubmission(models.Model):

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assignment_submissions",
    )

    answer = models.TextField(
        blank=True,
    )

    link = models.URLField(
        blank=True,
    )

    file = models.FileField(
        upload_to="assignment_submissions/",
        blank=True,
        null=True,
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("-created_at",)

        constraints = (
            models.UniqueConstraint(
                fields=("assignment", "student"),
                name="unique_assignment_student_submission",
            ),
        )

    def __str__(self):
        return (
            f"{self.student.username} — "
            f"{self.assignment.title}"
        )


# =========================================================
# GRADE
# =========================================================

class Grade(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_grades",
    )

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="grades",
        null=True,
        blank=True,
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="grades",
    )

    score = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.student.username} — "
            f"{self.subject.name} — "
            f"{self.score}"
        )


# =========================================================
# DIRECT MESSAGES
# =========================================================

class Message(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )

    content = models.TextField()

    is_read = models.BooleanField(
        default=False,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.sender.username} → "
            f"{self.receiver.username}"
        )


# =========================================================
# COMMUNITY POST
# =========================================================

class CommunityPost(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="community_posts",
    )

    title = models.CharField(
        max_length=200,
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_announcement = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# =========================================================
# COMMUNITY COMMENT
# =========================================================

class CommunityComment(models.Model):

    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="community_comments",
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"{self.author.username} - "
            f"{self.post.title}"
        )


# =========================================================
# COMMUNITY MESSAGE
# =========================================================

class CommunityMessage(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="community_messages",
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"{self.sender.username}: "
            f"{self.content[:40]}"
        )


# =========================================================
# COMMUNITY NOTIFICATION
# =========================================================

class CommunityNotification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="community_notifications",
    )

    message = models.ForeignKey(
        CommunityMessage,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    is_read = models.BooleanField(
        default=False,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = (
            models.UniqueConstraint(
                fields=("user", "message"),
                name="unique_community_notification",
            ),
        )

    def __str__(self):
        return (
            f"{self.user.username} — "
            f"Community notification"
        )


# =========================================================
# SELF STUDY — VOCABULARY SET
# =========================================================

class VocabularySet(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vocabulary_sets",
    )

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


# =========================================================
# SELF STUDY — VOCABULARY
# =========================================================

class Vocabulary(models.Model):

    class Level(models.TextChoices):

        A1 = "A1", "A1"
        A2 = "A2", "A2"
        B1 = "B1", "B1"
        B2 = "B2", "B2"
        C1 = "C1", "C1"
        C2 = "C2", "C2"

    # -----------------------------------------------------
    # SET
    # -----------------------------------------------------

    vocabulary_set = models.ForeignKey(
        VocabularySet,
        on_delete=models.CASCADE,
        related_name="words",
        null=True,
        blank=True,
    )

    # -----------------------------------------------------
    # WORD
    # -----------------------------------------------------

    word = models.CharField(
        max_length=100,
    )

    # -----------------------------------------------------
    # UZBEK TRANSLATION
    # -----------------------------------------------------

    translation = models.CharField(
        max_length=200,
    )

    # -----------------------------------------------------
    # PRONUNCIATION
    # -----------------------------------------------------

    pronunciation = models.CharField(
        max_length=200,
        blank=True,
    )

    # -----------------------------------------------------
    # DEFINITION
    # -----------------------------------------------------

    definition = models.TextField()

    # -----------------------------------------------------
    # OPTIONAL INFORMATION
    # -----------------------------------------------------

    example = models.TextField(
        blank=True,
    )

    synonyms = models.TextField(
        blank=True,
    )

    # -----------------------------------------------------
    # LEVEL
    # -----------------------------------------------------

    level = models.CharField(
        max_length=2,
        choices=Level.choices,
        default=Level.B1,
        db_index=True,
    )

    # -----------------------------------------------------
    # CATEGORY
    # -----------------------------------------------------

    category = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    # -----------------------------------------------------
    # OWNER
    # -----------------------------------------------------

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_vocabularies",
    )

    # -----------------------------------------------------
    # VISIBILITY
    # -----------------------------------------------------

    is_public = models.BooleanField(
        default=True,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    # -----------------------------------------------------
    # DATES
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("word",)

    def __str__(self):
        return self.word


# =========================================================
# VOCABULARY FAVORITE
# =========================================================

class VocabularyFavorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vocabulary_favorites",
    )

    vocabulary = models.ForeignKey(
        Vocabulary,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-created_at",)

        constraints = (
            models.UniqueConstraint(
                fields=("user", "vocabulary"),
                name="unique_vocabulary_favorite",
            ),
        )

    def __str__(self):
        return (
            f"{self.user.username} — "
            f"{self.vocabulary.word}"
        )


# =========================================================
# VOCABULARY PROGRESS
# =========================================================

class VocabularyProgress(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vocabulary_progress",
    )

    vocabulary = models.ForeignKey(
        Vocabulary,
        on_delete=models.CASCADE,
        related_name="user_progress",
    )

    is_learned = models.BooleanField(
        default=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("-updated_at",)

        constraints = (
            models.UniqueConstraint(
                fields=("user", "vocabulary"),
                name="unique_vocabulary_progress",
            ),
        )

    def __str__(self):
        return (
            f"{self.user.username} — "
            f"{self.vocabulary.word}"
        )






# =========================================================
# READING PRACTICE
# =========================================================

class ReadingPassage(models.Model):

    class Level(models.TextChoices):
        A1 = "A1", "A1"
        A2 = "A2", "A2"
        B1 = "B1", "B1"
        B2 = "B2", "B2"
        C1 = "C1", "C1"

    title = models.CharField(max_length=200)

    level = models.CharField(
        max_length=2,
        choices=Level.choices,
        default=Level.B1,
    )

    topic = models.CharField(
        max_length=100,
        blank=True,
    )

    text = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["level", "title"]

    def __str__(self):
        return f"{self.title} ({self.level})"




class ReadingQuestion(models.Model):

    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = "MCQ", "Multiple Choice"
        TRUE_FALSE_NOT_GIVEN = "TFNG", "True / False / Not Given"
        YES_NO_NOT_GIVEN = "YNNG", "Yes / No / Not Given"
        SHORT_ANSWER = "SHORT", "Short Answer"
        SENTENCE_COMPLETION = "SENTENCE", "Sentence Completion"
        SUMMARY_COMPLETION = "SUMMARY", "Summary Completion"
        NOTE_COMPLETION = "NOTE", "Note Completion"
        TABLE_COMPLETION = "TABLE", "Table Completion"
        MATCHING_HEADINGS = "HEADINGS", "Matching Headings"
        MATCHING_INFORMATION = "INFORMATION", "Matching Information"
        MATCHING_FEATURES = "FEATURES", "Matching Features"

    passage = models.ForeignKey(
        ReadingPassage,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    question_type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.MULTIPLE_CHOICE,
    )

    question = models.TextField()

    option_a = models.CharField(
        max_length=300,
        blank=True,
    )

    option_b = models.CharField(
        max_length=300,
        blank=True,
    )

    option_c = models.CharField(
        max_length=300,
        blank=True,
    )

    option_d = models.CharField(
        max_length=300,
        blank=True,
    )

    correct_answer = models.CharField(
        max_length=300,
    )

    explanation = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.question[:80]




class QuizQuestion(models.Model):
    class Level(models.TextChoices):
        A1 = "A1", "A1 Beginner"
        A2 = "A2", "A2 Elementary"
        B1 = "B1", "B1 Intermediate"
        B2 = "B2", "B2 Upper-Intermediate"
        C1 = "C1", "C1 Advanced"
        C2 = "C2", "C2 Proficient"

    class Difficulty(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"

    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ],
    )

    explanation = models.TextField(blank=True)

    level = models.CharField(
        max_length=2,
        choices=Level.choices,
        db_index=True,
    )

    topic = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["level", "id"]

    def __str__(self):
        return f"{self.level} — {self.question[:70]}"
