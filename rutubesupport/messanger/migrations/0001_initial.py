# Generated by Django 5.1.1 on 2024-09-23 02:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chat",
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
                ("name", models.CharField(max_length=1000)),
                ("creator_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Message",
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
                ("value", models.CharField(max_length=1000000)),
                (
                    "date",
                    models.DateTimeField(blank=True, default=datetime.datetime.now),
                ),
                ("user_id", models.IntegerField()),
                ("chat_id", models.IntegerField()),
            ],
        ),
    ]
