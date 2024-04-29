from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    POSITION_CHOICES = (
        ("Developer", "Developer"),
        ("Project Manager", "Project Manager"),
        ("QA", "QA"),
        ("Designer", "Designer"),
        ("DevOps", "DevOps"),
    )

    name = models.CharField(max_length=64, choices=POSITION_CHOICES)


class Title(models.Model):
    TITLE_CHOICES = (
        ("Team Lead", "Team Lead"),
        ("Technical Lead", "Technical Lead"),
        ("CTO", "CTO"),
    )

    name = models.CharField(max_length=64, choices=TITLE_CHOICES)


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    phone_number = models.CharField(max_length=20, null=True, blank=True)
    telegram = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(
        upload_to="media",
        null=True,
        blank=True,
        unique=True,
        help_text="Upload your photo"
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.username} ({self.position})"

    def get_absolute_url(self):
        return reverse("users:worker-detail", kwargs={"pk": self.pk})


class Supervisor(Worker):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "supervisor"
        verbose_name_plural = "supervisors"

    def __str__(self):
        return f"{self.username} ({self.title})"
