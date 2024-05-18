from django.conf import settings
from django.db import models

from users.models import WorkerUser


class Comment(models.Model):
    text = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        WorkerUser,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"{self.text} by {self.author}"


class TackStatus(models.TextChoices):
    CREATED = "Created", "Created"
    IN_PROGRESS = "In progress", "In progress"
    CHECKING = "Checking", "Checking"
    DONE = "Done", "Done"


class TaskType(models.TextChoices):
    INDEFINITE = "Indefinite", "Indefinite"
    BUG = "Bug", "Bug"
    NEW_FEATURE = "New feature", "New feature"
    BREAKING_CHANGE = "Breaking change", "Breaking change"
    REFACTORING = "Refactoring", "Refactoring"
    QA = "Q&A", "Q&A"


class TaskPriority(models.TextChoices):
    LOW = "Low", "Low"
    MEDIUM = "Medium", "Medium"
    HIGH = "High", "High"
    CRITICAL = "Critical", "Critical"


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=1024)
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        WorkerUser,
        on_delete=models.CASCADE,
        related_name="author_tasks"
    )
    status = models.CharField(
        max_length=64, choices=TackStatus.choices, default=TackStatus.CREATED
    )
    type = models.CharField(
        max_length=64, choices=TaskType.choices, default=TaskType.INDEFINITE
    )
    priority = models.CharField(
        max_length=64, choices=TaskPriority.choices, default=TaskPriority.LOW
    )
    responsible_workers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="worker_tasks"
    )
    comments = models.ManyToManyField(Comment, related_name="tasks")

    class Meta:
        ordering = ["-created"]
        verbose_name = "task"
        verbose_name_plural = "tasks"

    def __str__(self):
        return f"{self.name}"


class ProjectStatus(models.TextChoices):
    DEVELOPING = "Developing", "Developing"
    TESTING = "Testing", "Testing"
    DEBUGGING = "Debugging", "Debugging"
    DEPLOYING = "Deploying", "Deploying"


class Project(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=1024)
    status = models.CharField(
        max_length=64,
        choices=ProjectStatus.choices,
        default=ProjectStatus.DEVELOPING
    )
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    project_lead = models.ForeignKey(
        WorkerUser,
        on_delete=models.CASCADE,
        related_name="lead_projects",
        null=True,
        blank=True
    )
    responsible_workers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="workers_projects",
        blank=True,
        null=True
    )
    tasks = models.ManyToManyField(
        Task, related_name="project_tasks", blank=True, null=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "project"
        verbose_name_plural = "projects"

    def __str__(self):
        return f"{self.name} by {self.project_lead}"
