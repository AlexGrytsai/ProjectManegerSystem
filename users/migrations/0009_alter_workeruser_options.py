# Generated by Django 5.0.4 on 2024-05-22 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_workeruser_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="workeruser",
            options={
                "ordering": ["username"],
                "verbose_name": "worker",
                "verbose_name_plural": "workers",
            },
        ),
    ]
