from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.TextChoices):
    UNCONFIRMED = "Unconfirmed", "Unconfirmed"
    DEVELOPER = "Developer", "Developer"
    PROJECT_MANAGER = "Project Manager", "Project Manager"
    QA = "QA", "QA"
    DESIGNER = "Designer", "Designer"
    DEVOPS = "DevOps", "DevOps"


class Title(models.TextChoices):
    UNCONFIRMED = "Unconfirmed", "Unconfirmed"
    ENGINEER = "Engineer", "Engineer"
    MANAGER = "Manager", "Manager"
    TEAM_LEAD = "Team Lead", "Team Lead"
    TECHNICAL_LEAD = "Technical Lead", "Technical Lead"
    CTO = "CTO", "CTO"


class WorkerUser(AbstractUser):
    title = models.CharField(
        max_length=64, choices=Title.choices, default=Title.UNCONFIRMED
    )
    position = models.CharField(
        max_length=64, choices=Position.choices, default=Title.UNCONFIRMED
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

    is_supervisor = models.BooleanField(
        default=False,
        help_text="Defines or will have access to special "
                  "supervisor permissions"
    )

    def __str__(self):
        return f"{self.username}"

    def get_absolute_url(self):
        return reverse("users:worker-detail", kwargs={"pk": self.pk})


class Supervisor(models.Model):
    user = models.OneToOneField(
        WorkerUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    class Meta:
        verbose_name = "supervisor"
        verbose_name_plural = "supervisors"


class Worker(models.Model):
    user = models.OneToOneField(
        WorkerUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
