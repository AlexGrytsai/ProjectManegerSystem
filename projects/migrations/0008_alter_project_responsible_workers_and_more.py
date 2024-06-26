# Generated by Django 5.0.4 on 2024-05-27 05:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0007_alter_comment_options_alter_project_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="responsible_workers",
            field=models.ManyToManyField(
                related_name="workers_projects", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="tasks",
            field=models.ManyToManyField(
                related_name="project_tasks", to="projects.task"
            ),
        ),
    ]
