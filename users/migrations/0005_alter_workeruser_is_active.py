# Generated by Django 5.0.4 on 2024-05-07 11:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_workeruser_telegram"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workeruser",
            name="is_active",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether this user should "
                          "be treated as active. ",
            ),
        ),
    ]
