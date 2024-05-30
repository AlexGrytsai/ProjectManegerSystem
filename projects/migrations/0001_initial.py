# Generated by Django 5.0.4 on 2024-05-08 08:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(max_length=255)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "comment",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, unique=True)),
                ("description", models.TextField(max_length=1024)),
                ("deadline", models.DateField(blank=True, null=True)),
                ("is_completed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Created", "Created"),
                            ("In progress", "In progress"),
                            ("Checking", "Checking"),
                            ("Done", "Done"),
                        ],
                        default="Created",
                        max_length=64,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Indefinite", "Indefinite"),
                            ("Bug", "Bug"),
                            ("New feature", "New feature"),
                            ("Breaking change", "Breaking change"),
                            ("Refactoring", "Refactoring"),
                            ("Q&A", "Q&A"),
                        ],
                        default="Indefinite",
                        max_length=64,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("Low", "Low"),
                            ("Medium", "Medium"),
                            ("High", "High"),
                            ("Critical", "Critical"),
                        ],
                        default="Low",
                        max_length=64,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "comments",
                    models.ManyToManyField(related_name="tasks",
                                           to="projects.comment"),
                ),
                (
                    "responsible_workers",
                    models.ManyToManyField(
                        related_name="tasks", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "task",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, unique=True)),
                ("description", models.TextField(max_length=1024)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Developing", "Developing"),
                            ("Testing", "Testing"),
                            ("Debugging", "Debugging"),
                            ("Deploying", "Deploying"),
                        ],
                        default="Developing",
                        max_length=64,
                    ),
                ),
                ("deadline", models.DateField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "project_lead",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "responsible_workers",
                    models.ManyToManyField(
                        related_name="projects", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "tasks",
                    models.ManyToManyField(related_name="projects",
                                           to="projects.task"),
                ),
            ],
            options={
                "verbose_name": "project",
                "ordering": ["-created"],
            },
        ),
    ]
