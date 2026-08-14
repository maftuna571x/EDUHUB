from django.db import models


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


class Group(models.Model):
    name = models.CharField(
        max_length=50,
    )

    teacher = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="teaching_groups",
    )

    students = models.ManyToManyField(
        "users.User",
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
        "users.User",
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


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )

    student = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="assignment_submissions",
    )

    answer = models.TextField(
        blank=True,
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
        return f"{self.student.username} — {self.assignment.title}"


class Grade(models.Model):
    student = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="grades",
    )

    teacher = models.ForeignKey(
        "users.User",
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