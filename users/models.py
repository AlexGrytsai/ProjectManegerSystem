from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Position(models.TextChoices):
    GUEST = "Guest", "Guest"
    DEVELOPER = "Developer", "Developer"
    PROJECT_MANAGER = "Project Manager", "Project Manager"
    PRODUCT_MANAGER = "Product Manager", "Product Manager"
    QA = "QA", "QA"
    DESIGNER = "Designer", "Designer"
    DEVOPS = "DevOps", "DevOps"
    TEAM_LEAD = "Team Lead", "Team Lead"


class Role(models.TextChoices):
    GUEST = "Guest", "Guest"
    ENGINEER_MANAGER = "Engineer/Manager", "Engineer/Manager"
    SUPERVISOR = "Supervisor", "Supervisor"


class WorkerUser(AbstractUser):
    role = models.CharField(
        max_length=64, choices=Role.choices, default=Role.GUEST
    )
    position = models.CharField(
        max_length=64, choices=Position.choices, default=Position.GUEST
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        unique=True,
        help_text="Phone number (+3XX XXX XXX XXX)"
    )
    telegram = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        unique=True,
        help_text="Telegram username (@username)"
    )
    photo = models.ImageField(
        upload_to="media/users/photos/",
        null=True,
        blank=True,
        unique=False,
        help_text="Upload your photo",
    )

    is_supervisor = models.BooleanField(
        default=False,
        help_text="Defines or will have access to special "
                  "supervisor permissions"
    )

    def clean(self):
        super().clean()
        if self.phone_number:
            if not self.phone_number.startswith('+3'):
                raise ValidationError("Phone number should start with '+3'.")
            if not self.phone_number[1:].isdigit():
                raise ValidationError(
                    "Phone number should contain only digits after '+3'.")
            if len(self.phone_number) < 5:
                raise ValidationError("Phone number is too short.")
            if len(self.phone_number) > 16:
                raise ValidationError("Phone number is too long.")

        if self.telegram:
            if not self.telegram.startswith("@"):
                raise ValidationError(
                    "Telegram username should start with '@'.")
            if len(self.telegram) < 2:
                raise ValidationError("Telegram username is too short.")

            self.telegram = self.telegram[1:]

        if self.photo:
            max_photo_size = 2097152
            if self.photo.size > max_photo_size:
                raise ValidationError(
                    f"Photo size is too large "
                    f"(max. {max_photo_size/1024/1024}MB)"
                )

    def __str__(self):
        return f"{self.username}"

    def get_absolute_url(self):
        return reverse("users:worker-detail", kwargs={"pk": self.pk})
