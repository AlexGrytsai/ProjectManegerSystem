from django.conf import settings
from django.db import models

from users.models import WorkerUser


class Comment(models.Model):
    text = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(WorkerUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]
        verbose_name = "comment"

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
    author = models.ForeignKey(WorkerUser, on_delete=models.CASCADE)
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
        settings.AUTH_USER_MODEL, related_name="tasks"
    )
    comments = models.ManyToManyField(Comment, related_name="tasks")

    class Meta:
        ordering = ["-created"]
        verbose_name = "task"

    def __str__(self):
        return f"{self.name} by {self.author}"


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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    project_lead = models.ForeignKey(WorkerUser, on_delete=models.CASCADE)
    responsible_workers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="projects"
    )
    tasks = models.ManyToManyField(Task, related_name="projects")

    class Meta:
        ordering = ["-created"]
        verbose_name = "project"

    def __str__(self):
        return f"{self.name} by {self.author}"
