# Generated by Django 5.0.4 on 2024-05-25 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_workeruser_last_activity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workeruser",
            name="last_activity",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
